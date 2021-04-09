from collections import defaultdict
import json
import itertools as it
import streamlit as st
from annotated_text import annotated_text


widget_height = st.sidebar.number_input("Widget Size", 200, 1200)


docs = defaultdict(dict)
for fname, dataset in [("ner_predictions.jsonl", "predicted"),
                       ("test.jsonl", "annotation")]:
    with open(fname) as f:
        for line in f:
            record = json.loads(line)
            docs[record["doc_id"]][dataset] = record
doc_ids = list(docs.keys())
doc_id_selection = st.selectbox("Choose a document", doc_ids)
dataset = st.radio("Type", ["predicted", "annotation"])
j = docs[doc_id_selection][dataset]
words = j["words"]
ners = j["ner"]
words_with_ner_annot = [{"word": word, "id": None} for word in words]
id2type = {None: None}
for id_, (start, stop, type_) in enumerate(ners):
    for ii in range(start, stop):
        words_with_ner_annot[ii]["id"] = id_
        id2type[id_] = type_
colors = {
    "Material": "#fea",
    "Method": "#faa",
    "Metric": "#afa",
    "Task": "#8ef",
}
spans = []
for id_, groupby in it.groupby(words_with_ner_annot, key=lambda x: x["id"]):
    type_ = id2type[id_]
    text = " ".join([w["word"] for w in groupby])
    if type_ is None:
        spans.append(text)
    else:
        spans.append((text, type_, colors[type_]))
offset = int(st.number_input("Offset", min_value=0, max_value=len(spans)))
annotated_text(*spans[offset:], height=widget_height)