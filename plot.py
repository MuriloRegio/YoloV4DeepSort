import plotly.graph_objs as go
import pandas as pd


t1 = pd.read_csv('results.tsv', sep=',')
t2 = pd.read_csv('new_results.csv', sep=',')

getAmountP = lambda df, c : ((df['Conflicts'] > 0) & (df['Class'] == c)).sum()
getAmountN = lambda df, c : ((df['Conflicts'] == 0) & (df['Class'] == c)).sum()

FP1 = getAmountP(t1,0)
TP1 = getAmountP(t1,1)
FN1 = getAmountN(t1,1)
TN1 = getAmountN(t1,0)

FP2 = getAmountP(t2,0)
TP2 = getAmountP(t2,1)
FN2 = getAmountN(t2,1)
TN2 = getAmountN(t2,0)

print (TP1 + FN1)
print (TP2 + FN2)

print (FP1 + TN1)
print (FP2 + TN2)

labels = ["None", "At least 1"]

b1N = go.Bar(x=[["Alpha=1.5"]*2, labels], y=[TN1, FP1], name='Non-Violent', marker_color="#EF553B")
b1P = go.Bar(x=[["Alpha=1.5"]*2, labels], y=[FN1, TP1], name='Violent', marker_color="#636EFA")

b2N = go.Bar(x=[["Alpha=1"]*2, labels], y=[TN2, FP2], name='Non-Violent', marker_color="#EF553B",showlegend=False)
b2P = go.Bar(x=[["Alpha=1"]*2, labels], y=[FN2, TP2], name='Violent', marker_color="#636EFA",showlegend=False)

traces = [b2N, b2P, b1N, b1P]

layout = go.Layout(
	title='Detected Personal Space invasions per Video Type and Alpha',
	yaxis=dict(
		title='Number of Videos',
		gridcolor='#aaaaaa',
	),
	xaxis=dict(
		title='Personal Space invasions on the Video',
		showgrid=False,
	),
	plot_bgcolor='#ffffff',
	title_x=0.5,
	barmode="stack"
)


fig = go.Figure(data=traces, layout=layout)
fig.show()