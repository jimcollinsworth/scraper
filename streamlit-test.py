import streamlit as st
from pandas import read_csv
from plotnine import (
    aes,
    geom_histogram,
    geom_point,
    ggplot,
    scale_x_log10,
    scale_y_log10,
    theme_bw,
)

if "random_state" not in st.session_state:
    st.session_state.random_state = 0


def update_random_state():
    st.session_state.random_state += 1


with st.sidebar:
    sample_ui = st.number_input(
        "sample", 0.0, 1.0, value=0.1, step=0.01, on_change=update_random_state
    )
    log = st.checkbox("Log Scale")


@st.cache_data
def load_data():
    df = read_csv(
        "https://raw.githubusercontent.com/GShotwell/streamlit-shiny-comp/main/nyc-taxi.csv"
    )
    return df


data = load_data()


def take_sample_uncached(df, fraction):
    return df.copy().sample(frac=fraction, random_state=st.session_state.random_state)


def tip_plot(sample, log=False):
    plot = ggplot(sample, aes("tip_amount", "total_amount")) + geom_point() + theme_bw()
    if log:
        plot = plot + scale_x_log10() + scale_y_log10()
    return plot


def amount_histogram(df):
    plot = ggplot(df, aes(x="total_amount")) + geom_histogram(binwidth=5) + theme_bw()
    return plot


def plot(sampled, log=False):
    st.subheader(f'First taxi id: {sampled["taxi_id"].iloc[0]}')

    tips = tip_plot(sampled, log=log)
    st.pyplot(tips.draw())

    amounts = amount_histogram(sampled)
    st.pyplot(amounts.draw())


sampled = take_sample_uncached(data, sample_ui)
plot(sampled, log=log)