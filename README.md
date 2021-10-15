# Ideoscope

An ideoscope (noun. /aɪdɪɒskoʊp/, plural: ideoscopes) is an instrument for measuring your thought process through a host of novel metrics. It builds on top of the conceptarium and provides a window into your thinking in the form of an analytics dashboard full of stats and visualizations. Quantifying your thought process paves the way for a more intimate understanding of your thought patterns as a knowledge worker. The process of measurement, in turn, enables a host of strategies for nurturing your mind, such as A/B testing your routine for maximum generation of novel ideas (i.e. ideogenesis) or setting monthly goals for the breadth of your perspective (i.e. memetic variability).

[Read more...](https://paulbricman.com/thoughtware/ideoscope)

# Installation

The ideoscope is can either be deployed from source or using Docker.

### Docker

To deploy the conceptarium using Docker, first make sure to have it installed, then simply run the following.

```
docker run -p 8501:8501 paulbricman/ideoscope 
```

Your ideoscope should be available at `localhost:8501`.

### From Source

To set up the ideoscope, clone the repository and run the following:

```
python3 -m pip install -r requirements.txt
python3 -m textblob.download_corpora
streamlit run main.py
```

Your ideoscope should be available at `localhost:8501`.