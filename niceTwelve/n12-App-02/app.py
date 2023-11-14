import pandas as pd
from nicegui import ui as nui
from nicegui import app
# from matplotlib import pyplot as plt
import plotly.express as px


# Set the static files location
images = app.add_static_files("/images", "images")


# Set a data storage class:
class NucleotideCounter:
    """
    Class to interpret and act as a psuedo-api
    """
    def __init__(self, sequence=''):
        # I like template more than I like rewriting stuff.
        self.nTemplate = "There are {} {}."
        self.nameTransform = {"A": "adenine", "T": "thymine", "G": "guanine", "C": "cytosine"}
        self.columnNames = ['Nucleotide', 'Count']
        self.rows = []
        self.d = {}
        
        self.sequence = sequence
        if len(sequence) > 0:
            self.update(sequence)
            self.self.rebuildTable()


    def dnaNucleotideCount(self, seq):
        # Custom function to count the letters in the nucleotides:
        d = dict(
            [
                ("A", seq.count("A")),
                ("T", seq.count("T")),
                ("G", seq.count("G")),
                ("C", seq.count("C")),
            ]
        )

        self.d = d

    def update(self, newSequence):
        """Update the counts and text"""
        self.sequence = newSequence
        self.dnaNucleotideCount(newSequence)
        self.TText = self.nTemplate.format( self.d['T'], self.nameTransform['T'])
        self.CText = self.nTemplate.format( self.d['C'], self.nameTransform['C'])
        self.AText = self.nTemplate.format( self.d['A'], self.nameTransform['A'])
        self.GText = self.nTemplate.format( self.d['G'], self.nameTransform['G'])

    def rebuildTable(self):
        if self.d:
            self.rows = []

            df = pd.DataFrame.from_dict(self.d, orient='index')
            df.reset_index(inplace=True)
            df.columns = self.columnNames
            self.rows = df.to_dict('records')



def recount(e):
    sequence = str(e.value)
    # I don't like functions doing more than one thing
    dna.update(sequence)
    result.set_text(sequence)

def update():
    # Force the table to be empty before updating it:
    tideCount.rows = []
    dna.rebuildTable()
    tideCount.add_rows(*dna.rows)

def updateChart():
    idf = pd.DataFrame.from_dict(data=dna.d, orient='index')
    idf.reset_index(inplace=True)
    idf.columns = dna.columnNames
    fig = px.bar(
        idf,
        x=dna.columnNames[0],
        y=dna.columnNames[1],
        title='Counts of Nucleotides',
        color_discrete_sequence=['seagreen']
    )
    figure = nui.plotly(fig).classes('h-150 w-100')
    figure.update()


with nui.header().style((
    "color: ##bdbdbd;"
    "background-color: #424242;"
    "font-weight: 600;"
    "font-size: 18px"
    )).props("elevated"):
        nui.label("DNA Nucleotide Count Web App")  # .style('margin:auto;')

nui.image("./images/dna-logo.jpg").style(
    ("height: 50%;" "width: 50%")
)  ##style('margin:auto;')
nui.label(
    "This app counts the nucleotide composition of query DNA!"
)  # .style('margin:auto;')

nui.separator()

nui.textarea(
    label="Text",
    placeholder="Insert DNA Nucleotide Sequence",
    on_change=lambda e: recount(e)
).style("height: 150%; width: 55%")

nui.markdown("## Input (DNA Query):")
result = nui.label()
nui.markdown(("## Output (Nucleotide Count):"))

dna = NucleotideCounter(result.text)

## Print Text:
nui.markdown("### 2. Print Text")
with nui.column():
    a = nui.label().bind_text_from(dna, 'AText')
    c = nui.label().bind_text_from(dna, 'CText')
    g = nui.label().bind_text_from(dna, 'GText')
    t = nui.label().bind_text_from(dna, 'TText')


nui.markdown('### 3. Display Dataframe:')

tideCount = nui.table(
    columns=[{'name': col, 'label': col, 'field': col} for col in dna.columnNames],
    rows=dna.rows)

# This is not ideal but I need this working at this point.
nui.button('Update', on_click=update)

nui.markdown('### 4. Bar Plot:')


fig = px.bar()
figure = nui.plotly(fig).set_visibility(False)
nui.button('Update', on_click=updateChart)

## Fin.
nui.run(dark=True, port=7860)
