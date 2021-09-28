from bokeh.plotting import figure
from bokeh.models import LinearAxis, Range1d, HoverTool, ColumnDataSource, Legend
from bokeh.layouts import gridplot, column, row
from bokeh.models.widgets import Slider, CheckboxGroup, Div
from bokeh.io import curdoc
from tornado import gen

class Visual:
    def __init__(self, callbackFunc, running, sensorTimeoutMs):
        self.running = running # Store the current state of the Flag
        self.callbackFunc = callbackFunc # Store the callback function
        self.sensorTimeoutMs = sensorTimeoutMs

        self.plot_options = dict(plot_width=1200, plot_height=400)
        self.source, self.pAll = self.definePlot() # Define various plots. Return handles for data source (self.source) and combined plot (self.pAll)
        self.doc = curdoc() # Save curdoc() to make sure all threads see the same document. curdoc() refers to the Bokeh web document
        self.layout() # Set the checkboxes and overall layout of the webpage
        self.prev_y1 = 0

    def definePlot(self):
        # Define plot 1 to plot raw sensor data
        p1 = figure(**self.plot_options, y_range=(0, 4096), title="Sensor Data")
        p1.yaxis.axis_label = "Sensor Value"

        # Define plot 2 to plot (1) processed sensor data and (2) classification result at each time point
        p2 = figure(**self.plot_options, x_range=p1.x_range, y_range=(-1, 1), title="Computed Value") # Link x-axis of first and second graph
        p2.xaxis.axis_label = "Time (Discrete)"
        p2.yaxis.axis_label = "Computed Value"

        source = ColumnDataSource(data=dict(x=[0], ps1=[0], ps2=[0], ps3=[0], y1=[0]))

        ps1 = p1.line(x='x', y='ps1', source=source, color="firebrick", line_width=2)
        ps2 = p1.line(x='x', y='ps2', source=source, color="green", line_width=2)
        ps3 = p1.line(x='x', y='ps3', source=source, color="blue", line_width=2)

        legend = Legend(items=[("PS1", [ps1]), ("PS2", [ps2]), ("PS3", [ps3])], location=(5, 30))
        p1.add_layout(legend, 'right')
        p1.legend.click_policy = "hide"

        r1 = p2.line(x='x', y='y1', source=source, color="indigo", line_width=2) # Line plot for computed values

        pAll = gridplot([[p1], [p2]])

        return source, pAll

    @gen.coroutine
    def update(self, val):
        newx = self.source.data['x'][-1] + 1 # Increment the time step on the x-axis of the graphs
        ps1, ps2, ps3 = val

        if ps2 > 100 and ps3 > 100:
            y1 = (ps2 - ps3) / max(ps2, ps3)
        else:
            y1 = 0

        new_data = dict(x=[newx], ps1=[ps1], ps2=[ps2], ps3=[ps3], y1=[y1])

        self.source.stream(new_data, rollover=20) # Feed new data to the graphs and set the rollover period to be xx samples

    def checkbox1Handler(self, attr, old, new):
        if 0 in list(new):
            if 0 not in list(old):
                self.running.set()
                self.callbackFunc(self, self.running, self.sensorTimeoutMs) # Restart the Sensor thread
        else:
            self.running.clear()  # Kill the Sensor thread by clearing the Flag

    def sliderHandler(self, attr, old, new):
        self.sensorTimeoutMs = new

    def layout(self):
        checkbox1 = CheckboxGroup(labels=["start/stop"], active=[0])
        checkbox1.on_change('active', self.checkbox1Handler) # Specify the action to be performed upon change in checkboxes' values

        print(self.sensorTimeoutMs)
        slider = Slider(start=0, end=1000, value=self.sensorTimeoutMs, step=10, title='Sensor reading (ms, requires start/stop)')
        slider.on_change('value', self.sliderHandler)

        layout = row(column(checkbox1, slider, self.pAll))
        self.doc.add_root(layout) # Add the layout to the web document
