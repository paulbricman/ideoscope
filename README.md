![mockuper](https://user-images.githubusercontent.com/20104026/137454146-7f1d9c78-b833-4070-a3e9-7caa27cd4746.png)

# Ideoscope

An ideoscope (noun. /aɪdɪɒskoʊp/, plural: ideoscopes) is an instrument for measuring your thought process through a host of novel metrics. It builds on top of the conceptarium and provides a window into your thinking in the form of an analytics dashboard full of stats and visualizations. Quantifying your thought process paves the way for a more intimate understanding of your thought patterns as a knowledge worker. The process of measurement, in turn, enables a host of strategies for nurturing your mind, such as A/B testing your routine for maximum generation of novel ideas (i.e. memetic birth rate) or setting monthly goals for the breadth of your perspective (i.e. memetic variability).

[Read more...](https://paulbricman.com/thoughtware/ideoscope)

# Installation

**Note**: In order for the metrics to be decently informative, it's recommended that you use your conceptarium regularly for around 2 months before conducting an ideoscopy.

The ideoscope can either be deployed from source or using Docker.

**Note**: Some of the metrics computed by the ideoscope are significantly more compute-intensive than the day-by-day needs of the conceptarium. For instance, measures of semantic space coverage rely on sampling a huge number of random points and checking whether they manage to "hit" one of your thoughts (i.e. Monte Carlo approximation). For this reason, it's recommended that you run the ideoscope on at least consumer-grade hardware (i.e. not on a Raspberry Pi).

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

# Further Reading

- [conducting an ideoscopy](https://paulbricman.com/reflections/conducting-an-ideoscopy)
- [saving versus sampling](https://paulbricman.com/reflections/saving-versus-sampling)
- [ideoponics](https://paulbricman.com/reflections/ideoponics)
- [navigating worldviews](https://paulbricman.com/reflections/navigating-ideology)

# Screenshots

![mockuper(1)](https://user-images.githubusercontent.com/20104026/137455890-12ef95ce-b73a-4cb4-bdd0-c204621d2b58.png)

![mockuper(2)](https://user-images.githubusercontent.com/20104026/137455895-8972b555-b8f8-46e1-b5a4-4d355d25b5b9.png)

