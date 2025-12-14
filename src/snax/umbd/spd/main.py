import pandas as pd
import streamlit as st

import snax.umbd.spd.schema as schema
from snax.datasets import load_pandas


class SPD:

    def __init__(self):
        self.data = load_pandas(name="speed_dating", encoding="latin1")
        self.schema = schema


def main():
    app = StreamlitApp()
    app.layout()


st.markdown(
    """
<style>
    section[data-testid="stSidebar"] {
        width: 600px !important;  # Change this number (e.g. 350, 450, 500)
        min-width: 400px !important;
    }
</style>
""",
    unsafe_allow_html=True,
)


class StreamlitApp:
    def __init__(self):
        self.app = SPD()

    # @st.cache_data
    def load_data(self):
        return self.app.data

    def layout(self):
        st.title("Speed Dating Dataset")
        tab1, tab2 = st.tabs(["Explore", "Dataset Summary"])
        with tab1:
            with st.sidebar:
                st.button("Clear Selections", on_click=lambda: st.session_state.clear())
                columns = st.columns(len(schema.list_groups()))
                for ix, group in enumerate(schema.list_groups()):
                    with columns[ix]:
                        st.write(f"**{group.value}**")
                        for col in schema.list_by_group(group.value):
                            st.checkbox(col.name, key=col.name)
            cols = [
                key
                for key in st.session_state.keys()
                if st.session_state[key] is True and schema.exists(key)
            ]
            search_term = st.text_input("Search columns", "", key="live_search")
            st.write("### Columns")
            items = self.app.schema.to_list()
            if search_term:
                items = [
                    item
                    for item in self.app.schema.to_list()
                    if search_term.lower() in item.name.lower()
                    or search_term.lower() in item.desc.lower()
                    or search_term.lower() in ", ".join(item.tags or []).lower()
                ]
                st.write(f"Found {len(items)} matching columns")

            df = pd.DataFrame(
                {
                    "Column Name": [item.name for item in items],
                    "Description": [item.desc for item in items],
                    "Data Type": [item.dtype for item in items],
                    "Unique Values": [
                        self.app.data[item.name].nunique() for item in items
                    ],
                    "Samples": [
                        ", ".join(
                            map(
                                str,
                                self.app.data[item.name].dropna().unique()[:5].tolist(),
                            )
                        )
                        for item in items
                    ],
                    "Min/Mean/Max": [
                        (
                            f"{self.app.data[item.name].min()}/{self.app.data[item.name].mean():.2f}/{self.app.data[item.name].max()}"
                            if pd.api.types.is_numeric_dtype(self.app.data[item.name])
                            else "N/A"
                        )
                        for item in items
                    ],
                    "Num Missing": [
                        self.app.data[item.name].isna().sum() for item in items
                    ],
                }
            )
            if cols:
                df = df[df["Column Name"].isin(cols)]

            st.dataframe(df, use_container_width=True)
            # st.dataframe(self.app.dataset.data.select_dtypes("number").describe())
            # st.dataframe(self.app.dataset.data[cols].sample(10))
            st.divider()

            ccol1, ccol2 = st.columns(2)
            with ccol1:
                st.write("### Histograms")
                for col in cols:
                    try:
                        colname = schema.get_col_by_name(col).desc
                    except AttributeError:
                        colname = "N/A"

                    st.write(f"#### {col} ({colname})")
                    missing_count = self.app.data[col].isna().sum()
                    total_count = len(self.app.data[col])
                    bc1, bc2, bc3 = st.columns(3)
                    with bc1:
                        st.badge(f"Missing: {missing_count}", color="red")
                    with bc2:
                        st.badge(f"Total: {total_count}", color="blue")
                    with bc3:
                        st.badge(
                            f"Missing %: {missing_count / total_count * 100:.2f}%",
                            color="orange",
                        )
                    drop_nulls = st.checkbox(
                        "Drop Nulls", value=True, key=f"drop_nulls_{col}"
                    )
                    st.write(drop_nulls)
                    if drop_nulls:
                        hist_data = self.app.data[col].dropna()
                    else:
                        hist_data = self.app.data[col]

                    bar_chart_data = hist_data.value_counts()
                    st.write(bar_chart_data)
                    st.bar_chart(bar_chart_data, use_container_width=True)
            with ccol2:
                st.write("### Correlation Matrix")
                corr = self.app.data[cols].corr()
                st.dataframe(
                    corr.style.background_gradient(cmap="coolwarm"),
                    use_container_width=True,
                )
                # st.metric("Cell 1-1", "$1.2M", "12%")

        with tab2:
            c1, c2 = st.columns(2)
            with c1:
                st.write("### some filters")
                st.checkbox("Show only numeric columns", key="numeric_only")
            with c2:
                st.write("### Some other filters")
                st.checkbox("Show only categorical columns", key="categorical_only")
            st.write("### Data Types")
            st.dataframe(self.app.data.dtypes)


if __name__ == "__main__":
    main()
