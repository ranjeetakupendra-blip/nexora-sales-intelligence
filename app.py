import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ============================================================
# NEXORA — SALES INTELLIGENCE PLATFORM
# ============================================================

st.set_page_config(
    page_title="NEXORA | Sales Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# THEME
# ============================================================

PURPLE = "#7C3AED"
BLUE = "#2563EB"
CYAN = "#06B6D4"
GREEN = "#10B981"
RED = "#EF4444"

NAVY = "#172033"
TEXT = "#334155"
MUTED = "#64748B"
BG = "#F5F7FB"
WHITE = "#FFFFFF"
BORDER = "#E8EAF0"

# ============================================================
# GLOBAL STYLE
# ============================================================

st.markdown(
    f"""
    <style>

    .stApp {{
        background: {BG};
    }}

    section[data-testid="stSidebar"] {{
        background: {WHITE};
        border-right: 1px solid {BORDER};
    }}

    .block-container {{
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }}

    h1, h2, h3, h4 {{
        color: {NAVY} !important;
    }}

    p {{
        color: {TEXT};
    }}

    [data-testid="stMetric"] {{
        background: {WHITE};
        border: 1px solid {BORDER};
        border-radius: 18px;
        padding: 20px;
        box-shadow: 0 8px 25px rgba(31,41,55,0.06);
    }}

    [data-testid="stMetricLabel"] {{
        color: {MUTED} !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
    }}

    [data-testid="stMetricValue"] {{
        color: {NAVY} !important;
        font-size: 1.6rem !important;
        font-weight: 750 !important;
    }}

    [data-testid="stVerticalBlockBorderWrapper"] {{
        background: {WHITE};
        border: 1px solid {BORDER};
        border-radius: 20px;
        box-shadow: 0 8px 28px rgba(31,41,55,0.05);
    }}

    .stButton > button {{
        border-radius: 10px;
        border: 1px solid #DDD6FE;
        background: {WHITE};
        color: {PURPLE};
        font-weight: 600;
    }}

    .stButton > button:hover {{
        border-color: {PURPLE};
        color: {PURPLE};
    }}

    div[data-baseweb="select"] > div {{
        border-radius: 10px;
        border-color: {BORDER};
    }}

    hr {{
        border-color: {BORDER};
    }}

    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# DATA FILE
# ============================================================

def find_data_file():

    possible_files = [
        "processed_sales_data.csv",
        "sales_data.csv",
        "sales.csv",
        "data.csv"
    ]

    for filename in possible_files:

        if Path(filename).exists():
            return filename

    files = list(Path(".").glob("*.csv"))

    if files:
        return str(files[0])

    return None


data_file = find_data_file()

if data_file is None:

    st.error(
        "CSV dataset not found. Keep your sales CSV file "
        "inside the same folder as app.py."
    )

    st.stop()

# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv(data_file)

df["date"] = pd.to_datetime(
    df["date"],
    errors="coerce"
)

for column in [
    "quantity",
    "price",
    "promotion",
    "weekend",
    "sales"
]:

    if column in df.columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

df = df.dropna(
    subset=[
        "date",
        "sales"
    ]
)

if "quantity" not in df.columns:
    df["quantity"] = 0

if "product" not in df.columns:
    df["product"] = "Unknown"

if "promotion" not in df.columns:
    df["promotion"] = 0

if "weekend" not in df.columns:
    df["weekend"] = 0

# ============================================================
# FORMATTING
# ============================================================

def money(value):

    value = float(value)

    if abs(value) >= 1e7:
        return f"₹{value / 1e7:.2f}Cr"

    if abs(value) >= 1e5:
        return f"₹{value / 1e5:.2f}L"

    if abs(value) >= 1e3:
        return f"₹{value / 1e3:.1f}K"

    return f"₹{value:,.0f}"


def pct(value):

    return f"{value:.1f}%"

# ============================================================
# GLOBAL METRICS
# ============================================================

transactions = len(df)

total_revenue = df["sales"].sum()

units_sold = df["quantity"].sum()

avg_transaction = (
    total_revenue / transactions
    if transactions
    else 0
)

earliest_date = df["date"].min()

latest_date = df["date"].max()

# ============================================================
# PRODUCT METRICS
# ============================================================

product_revenue = (
    df.groupby("product")["sales"]
    .sum()
    .sort_values(
        ascending=False
    )
)

top_product = (
    product_revenue.index[0]
    if len(product_revenue)
    else "N/A"
)

top_product_revenue = (
    product_revenue.iloc[0]
    if len(product_revenue)
    else 0
)

top_product_share = (
    top_product_revenue
    / total_revenue
    * 100
    if total_revenue
    else 0
)

# ============================================================
# PROMOTION
# ============================================================

promo_avg = (
    df.loc[
        df["promotion"] == 1,
        "sales"
    ].mean()
    if (df["promotion"] == 1).any()
    else 0
)

normal_avg = (
    df.loc[
        df["promotion"] == 0,
        "sales"
    ].mean()
    if (df["promotion"] == 0).any()
    else 0
)

promo_revenue = df.loc[
    df["promotion"] == 1,
    "sales"
].sum()

promo_share = (
    promo_revenue
    / total_revenue
    * 100
    if total_revenue
    else 0
)

promo_difference = (
    (promo_avg - normal_avg)
    / normal_avg
    * 100
    if normal_avg
    else 0
)

# ============================================================
# WEEKEND
# ============================================================

weekend_avg = (
    df.loc[
        df["weekend"] == 1,
        "sales"
    ].mean()
    if (df["weekend"] == 1).any()
    else 0
)

weekday_avg = (
    df.loc[
        df["weekend"] == 0,
        "sales"
    ].mean()
    if (df["weekend"] == 0).any()
    else 0
)

weekend_revenue = df.loc[
    df["weekend"] == 1,
    "sales"
].sum()

weekend_share = (
    weekend_revenue
    / total_revenue
    * 100
    if total_revenue
    else 0
)

weekend_difference = (
    (weekend_avg - weekday_avg)
    / weekday_avg
    * 100
    if weekday_avg
    else 0
)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        f"""
        <div style="
            font-size:30px;
            font-weight:800;
            color:{PURPLE};
        ">
            ◈ NEXORA
        </div>
        """,
        unsafe_allow_html=True
    )

    st.caption(
        "SALES INTELLIGENCE PLATFORM"
    )

    st.success(
        "● SYSTEM ONLINE"
    )

    st.divider()

    page = st.radio(
        "WORKSPACE",
        [
            "Executive Overview",
            "Sales Analytics",
            "Product Intelligence",
            "Demand Forecast",
            "Business Insights"
        ]
    )

    st.divider()

    st.markdown(
        "**DATA STATUS**"
    )

    st.success(
        "● DATA CONNECTED"
    )

    st.caption(
        f"{transactions:,} transactions"
    )

    st.caption(
        f"{earliest_date.strftime('%d %b %Y')} → "
        f"{latest_date.strftime('%d %b %Y')}"
    )

    st.divider()

    st.caption(
        "NEXORA 2.0"
    )

    st.caption(
        "Sales Intelligence & Forecasting"
    )

# ============================================================
# HEADER
# ============================================================

st.title(
    "Good evening 👋"
)

st.caption(
    "Here's what's happening with your sales performance."
)

# ============================================================
# EXECUTIVE OVERVIEW
# ============================================================

if page == "Executive Overview":

    st.subheader(
        "Executive Overview"
    )

    st.caption(
        f"Business performance from "
        f"{earliest_date.strftime('%d %b %Y')} "
        f"to "
        f"{latest_date.strftime('%d %b %Y')}"
    )

    st.write("")

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.metric(
            "TOTAL REVENUE",
            money(total_revenue)
        )

    with k2:
        st.metric(
            "TRANSACTIONS",
            f"{transactions:,}"
        )

    with k3:
        st.metric(
            "UNITS SOLD",
            f"{units_sold:,.0f}"
        )

    with k4:
        st.metric(
            "AVG TRANSACTION",
            money(avg_transaction)
        )

    st.write("")

    # --------------------------------------------------------
    # REVENUE PERFORMANCE
    # --------------------------------------------------------

    left, right = st.columns([2.1, 1])

    with left:

        with st.container(border=True):

            st.subheader(
                "Revenue Performance"
            )

            daily = (
                df.groupby(
                    "date",
                    as_index=False
                )["sales"]
                .sum()
            )

            daily["7_day_avg"] = (
                daily["sales"]
                .rolling(7)
                .mean()
            )

            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=daily["date"],
                    y=daily["sales"],
                    mode="lines",
                    name="Daily Revenue",
                    line=dict(
                        color=PURPLE,
                        width=2
                    ),
                    fill="tozeroy",
                    fillcolor="rgba(124,58,237,0.08)"
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=daily["date"],
                    y=daily["7_day_avg"],
                    mode="lines",
                    name="7-Day Average",
                    line=dict(
                        color=CYAN,
                        width=3
                    )
                )
            )

            fig.update_layout(
                height=390,
                template="plotly_white",
                margin=dict(
                    l=10,
                    r=10,
                    t=10,
                    b=10
                ),
                xaxis_title=None,
                yaxis_title=None,
                hovermode="x unified"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    # --------------------------------------------------------
    # REVENUE MIX
    # --------------------------------------------------------

    with right:

        with st.container(border=True):

            st.subheader(
                "Revenue Mix"
            )

            fig = go.Figure(
                data=[
                    go.Pie(
                        labels=product_revenue.index,
                        values=product_revenue.values,
                        hole=0.68,
                        textinfo="none",
                        marker=dict(
                            colors=[
                                PURPLE,
                                BLUE,
                                CYAN,
                                "#A78BFA",
                                "#60A5FA"
                            ]
                        )
                    )
                ]
            )

            fig.add_annotation(
                text=(
                    f"<b>{money(total_revenue)}</b>"
                    "<br><span style='font-size:12px'>Revenue</span>"
                ),
                x=0.5,
                y=0.5,
                showarrow=False,
                font=dict(
                    size=16,
                    color=NAVY
                )
            )

            fig.update_layout(
                height=330,
                template="plotly_white",
                margin=dict(
                    l=5,
                    r=5,
                    t=5,
                    b=5
                )
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            st.markdown(
                f"**Top Product:** {top_product}"
            )

            st.caption(
                f"{pct(top_product_share)} of total revenue"
            )

    st.write("")

    # --------------------------------------------------------
    # PERFORMANCE SIGNALS
    # --------------------------------------------------------

    st.subheader(
        "Performance Signals"
    )

    st.caption(
        "Key business indicators from your sales data."
    )

    s1, s2, s3 = st.columns(3)

    with s1:

        with st.container(border=True):

            st.markdown(
                "### Promotion Performance"
            )

            st.metric(
                "REVENUE CONTRIBUTION",
                pct(promo_share)
            )

            st.progress(
                min(
                    max(promo_share / 100, 0),
                    1
                )
            )

            st.caption(
                f"Promotion revenue: "
                f"{money(promo_revenue)}"
            )

    with s2:

        with st.container(border=True):

            st.markdown(
                "### Weekend Contribution"
            )

            st.metric(
                "REVENUE CONTRIBUTION",
                pct(weekend_share)
            )

            st.progress(
                min(
                    max(weekend_share / 100, 0),
                    1
                )
            )

            st.caption(
                f"Weekend revenue: "
                f"{money(weekend_revenue)}"
            )

    with s3:

        with st.container(border=True):

            st.markdown(
                "### Top Product Contribution"
            )

            st.metric(
                "REVENUE CONTRIBUTION",
                pct(top_product_share)
            )

            st.progress(
                min(
                    max(top_product_share / 100, 0),
                    1
                )
            )

            st.caption(
                f"{top_product}: "
                f"{money(top_product_revenue)}"
            )

    st.write("")

    # --------------------------------------------------------
    # MONTHLY
    # --------------------------------------------------------

    with st.container(border=True):

        st.subheader(
            "Monthly Revenue Performance"
        )

        monthly = (
            df.assign(
                month=df["date"].dt.to_period("M")
            )
            .groupby(
                "month",
                as_index=False
            )["sales"]
            .sum()
        )

        monthly["month"] = (
            monthly["month"].astype(str)
        )

        fig = px.bar(
            monthly,
            x="month",
            y="sales",
            text_auto=".2s"
        )

        fig.update_traces(
            marker_color=PURPLE,
            textposition="outside"
        )

        fig.update_layout(
            height=390,
            template="plotly_white",
            xaxis_title=None,
            yaxis_title="Revenue"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# ============================================================
# SALES ANALYTICS
# ============================================================

elif page == "Sales Analytics":

    st.subheader(
        "Sales Analytics"
    )

    st.caption(
        "Explore revenue, volume and time-based performance."
    )

    st.write("")

    a, b, c, d = st.columns(4)

    with a:
        st.metric(
            "REVENUE",
            money(total_revenue)
        )

    with b:
        st.metric(
            "ORDERS",
            f"{transactions:,}"
        )

    with c:
        st.metric(
            "UNITS",
            f"{units_sold:,.0f}"
        )

    with d:
        st.metric(
            "AVG ORDER",
            money(avg_transaction)
        )

    st.write("")

    with st.container(border=True):

        st.subheader(
            "Daily Revenue Trend"
        )

        daily = (
            df.groupby(
                "date",
                as_index=False
            )["sales"]
            .sum()
        )

        fig = px.line(
            daily,
            x="date",
            y="sales"
        )

        fig.update_traces(
            line=dict(
                color=PURPLE,
                width=3
            )
        )

        fig.update_layout(
            height=430,
            template="plotly_white",
            xaxis_title=None,
            yaxis_title="Revenue",
            hovermode="x unified"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.write("")

    left, right = st.columns(2)

    with left:

        with st.container(border=True):

            st.subheader(
                "Monthly Revenue"
            )

            monthly = (
                df.assign(
                    month=df["date"].dt.to_period("M")
                )
                .groupby(
                    "month",
                    as_index=False
                )["sales"]
                .sum()
            )

            monthly["month"] = (
                monthly["month"].astype(str)
            )

            fig = px.bar(
                monthly,
                x="month",
                y="sales",
                text_auto=".2s"
            )

            fig.update_traces(
                marker_color=BLUE,
                textposition="outside"
            )

            fig.update_layout(
                height=380,
                template="plotly_white",
                xaxis_title=None,
                yaxis_title="Revenue"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    with right:

        with st.container(border=True):

            st.subheader(
                "Average Revenue by Day"
            )

            temp = df.copy()

            temp["day"] = (
                temp["date"].dt.day_name()
            )

            order = [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday"
            ]

            day_data = (
                temp.groupby("day")["sales"]
                .mean()
                .reindex(order)
                .reset_index()
            )

            fig = px.bar(
                day_data,
                x="day",
                y="sales"
            )

            fig.update_traces(
                marker_color=CYAN
            )

            fig.update_layout(
                height=380,
                template="plotly_white",
                xaxis_title=None,
                yaxis_title="Average Revenue"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    st.write("")

    with st.container(border=True):

        st.subheader(
            "Units Sold by Product"
        )

        units = (
            df.groupby(
                "product",
                as_index=False
            )["quantity"]
            .sum()
            .sort_values(
                "quantity",
                ascending=False
            )
        )

        fig = px.bar(
            units,
            x="product",
            y="quantity",
            text_auto=".2s"
        )

        fig.update_traces(
            marker_color=PURPLE,
            textposition="outside"
        )

        fig.update_layout(
            height=400,
            template="plotly_white",
            xaxis_title=None,
            yaxis_title="Units Sold"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# ============================================================
# PRODUCT INTELLIGENCE
# ============================================================

elif page == "Product Intelligence":

    st.subheader(
        "Product Intelligence"
    )

    st.caption(
        "Understand which products drive revenue and volume."
    )

    st.write("")

    product_data = (
        df.groupby("product")
        .agg(
            Revenue=("sales", "sum"),
            Units=("quantity", "sum"),
            Orders=("sales", "count"),
            Avg_Order=("sales", "mean")
        )
        .reset_index()
        .sort_values(
            "Revenue",
            ascending=False
        )
    )

    p1, p2, p3, p4 = st.columns(4)

    with p1:
        st.metric(
            "TOP PRODUCT",
            top_product
        )

    with p2:
        st.metric(
            "TOP REVENUE",
            money(top_product_revenue)
        )

    with p3:
        st.metric(
            "PRODUCTS",
            product_data.shape[0]
        )

    with p4:
        st.metric(
            "AVG ORDER",
            money(avg_transaction)
        )

    st.write("")

    with st.container(border=True):

        st.subheader(
            "Revenue by Product"
        )

        fig = px.bar(
            product_data,
            x="product",
            y="Revenue",
            text_auto=".2s"
        )

        fig.update_traces(
            marker_color=PURPLE,
            textposition="outside"
        )

        fig.update_layout(
            height=430,
            template="plotly_white",
            xaxis_title=None,
            yaxis_title="Revenue"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.write("")

    left, right = st.columns(2)

    with left:

        with st.container(border=True):

            st.subheader(
                "Product Revenue Mix"
            )

            fig = go.Figure(
                go.Pie(
                    labels=product_data["product"],
                    values=product_data["Revenue"],
                    hole=0.65,
                    textinfo="percent",
                    marker=dict(
                        colors=[
                            PURPLE,
                            BLUE,
                            CYAN,
                            "#A78BFA",
                            "#60A5FA"
                        ]
                    )
                )
            )

            fig.update_layout(
                height=410,
                template="plotly_white"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    with right:

        with st.container(border=True):

            st.subheader(
                "Product Volume"
            )

            volume_data = (
                product_data
                .sort_values(
                    "Units",
                    ascending=False
                )
            )

            fig = px.bar(
                volume_data,
                x="product",
                y="Units",
                text_auto=".2s"
            )

            fig.update_traces(
                marker_color=BLUE,
                textposition="outside"
            )

            fig.update_layout(
                height=410,
                template="plotly_white",
                xaxis_title=None,
                yaxis_title="Units Sold"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    st.write("")

    with st.container(border=True):

        st.subheader(
            "Product Performance Table"
        )

        display_data = product_data.copy()

        display_data["Revenue"] = (
            display_data["Revenue"]
            .apply(money)
        )

        display_data["Avg_Order"] = (
            display_data["Avg_Order"]
            .apply(money)
        )

        display_data.columns = [
            "Product",
            "Revenue",
            "Units",
            "Orders",
            "Average Order"
        ]

        st.dataframe(
            display_data,
            use_container_width=True,
            hide_index=True
        )

# ============================================================
# DEMAND FORECAST
# ============================================================

elif page == "Demand Forecast":

    st.subheader(
        "Demand Forecast"
    )

    st.caption(
        "AI-powered sales forecasting for future planning."
    )

    st.write("")

    # --------------------------------------------------------
    # CONFIGURATION
    # --------------------------------------------------------

    with st.container(border=True):

        st.markdown(
            "### Forecast Configuration"
        )

        col1, col2 = st.columns([1, 3])

        with col1:

            horizon = st.selectbox(
                "FORECAST HORIZON",
                [30, 90, 180, 365],
                index=0,
                format_func=lambda x:
                f"Next {x} Days"
            )

        with col2:

            st.info(
                f"◈ NEXORA will forecast the next "
                f"{horizon} days using historical "
                "sales patterns and seasonality."
            )

    st.write("")

    generate = st.button(
        "◈ Generate AI Forecast",
        use_container_width=True
    )

    # --------------------------------------------------------
    # EMPTY STATE
    # --------------------------------------------------------

    if not generate:

        with st.container(border=True):

            st.markdown(
                "### ◈ Ready to Forecast"
            )

            st.write(
                "Select a forecast horizon and generate "
                "an AI-powered demand prediction."
            )

        st.info(
            "The model analyses historical revenue, "
            "weekly behaviour and yearly seasonality."
        )

    # --------------------------------------------------------
    # GENERATE
    # --------------------------------------------------------

    else:

        try:

            from prophet import Prophet

            from sklearn.metrics import (
                mean_absolute_error,
                mean_squared_error
            )

            # -----------------------------------------------
            # PREPARE
            # -----------------------------------------------

            daily_sales = (
                df.groupby("date")["sales"]
                .sum()
                .reset_index()
            )

            prophet_data = (
                daily_sales.rename(
                    columns={
                        "date": "ds",
                        "sales": "y"
                    }
                )
            )

            # -----------------------------------------------
            # MODEL
            # -----------------------------------------------

            with st.spinner(
                "NEXORA AI is analysing sales patterns..."
            ):

                model = Prophet(
                    yearly_seasonality=True,
                    weekly_seasonality=True,
                    daily_seasonality=False
                )

                model.fit(
                    prophet_data
                )

                future = model.make_future_dataframe(
                    periods=horizon
                )

                forecast = model.predict(
                    future
                )

            # -----------------------------------------------
            # HISTORICAL METRICS
            # -----------------------------------------------

            historical = forecast[
                forecast["ds"].isin(
                    prophet_data["ds"]
                )
            ]

            actual = prophet_data["y"].values

            predicted = historical["yhat"].values

            mae = mean_absolute_error(
                actual,
                predicted
            )

            rmse = np.sqrt(
                mean_squared_error(
                    actual,
                    predicted
                )
            )

            # -----------------------------------------------
            # FUTURE
            # -----------------------------------------------

            future_forecast = forecast[
                forecast["ds"] > latest_date
            ].copy()

            projected_revenue = (
                future_forecast["yhat"].sum()
            )

            average_daily = (
                future_forecast["yhat"].mean()
            )

            peak_value = (
                future_forecast["yhat"].max()
            )

            lowest_value = (
                future_forecast["yhat"].min()
            )

            peak_row = future_forecast.loc[
                future_forecast["yhat"].idxmax()
            ]

            # -----------------------------------------------
            # SUMMARY
            # -----------------------------------------------

            st.markdown(
                "### Forecast Summary"
            )

            f1, f2, f3, f4 = st.columns(4)

            with f1:

                st.metric(
                    "PROJECTED REVENUE",
                    money(projected_revenue)
                )

            with f2:

                st.metric(
                    "AVG DAILY FORECAST",
                    money(average_daily)
                )

            with f3:

                st.metric(
                    "PEAK FORECAST",
                    money(peak_value)
                )

            with f4:

                st.metric(
                    "FORECAST PERIOD",
                    f"{horizon} Days"
                )

            st.write("")

            # -----------------------------------------------
            # CHART
            # -----------------------------------------------

            with st.container(border=True):

                st.subheader(
                    "Revenue Forecast"
                )

                st.caption(
                    "Historical performance versus projected future revenue."
                )

                fig = go.Figure()

                fig.add_trace(
                    go.Scatter(
                        x=prophet_data["ds"],
                        y=prophet_data["y"],
                        mode="lines",
                        name="Historical Revenue",
                        line=dict(
                            color=BLUE,
                            width=2.5
                        )
                    )
                )

                fig.add_trace(
                    go.Scatter(
                        x=future_forecast["ds"],
                        y=future_forecast["yhat"],
                        mode="lines",
                        name="AI Forecast",
                        line=dict(
                            color=PURPLE,
                            width=3
                        )
                    )
                )

                fig.add_trace(
                    go.Scatter(
                        x=(
                            list(
                                future_forecast["ds"]
                            )
                            +
                            list(
                                future_forecast["ds"]
                            )[::-1]
                        ),
                        y=(
                            list(
                                future_forecast["yhat_upper"]
                            )
                            +
                            list(
                                future_forecast["yhat_lower"]
                            )[::-1]
                        ),
                        fill="toself",
                        fillcolor="rgba(124,58,237,0.12)",
                        line=dict(
                            color="rgba(255,255,255,0)"
                        ),
                        name="Prediction Range"
                    )
                )

                fig.add_vline(
                    x=latest_date,
                    line_dash="dash",
                    line_color=MUTED,
                    annotation_text="Latest Data"
                )

                fig.update_layout(
                    height=500,
                    template="plotly_white",
                    hovermode="x unified",
                    xaxis_title=None,
                    yaxis_title="Revenue",
                    margin=dict(
                        l=10,
                        r=10,
                        t=20,
                        b=10
                    )
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            st.write("")

            # -----------------------------------------------
            # INTELLIGENCE
            # -----------------------------------------------

            st.subheader(
                "Forecast Intelligence"
            )

            i1, i2, i3 = st.columns(3)

            with i1:

                with st.container(border=True):

                    st.metric(
                        "PROJECTED REVENUE",
                        money(projected_revenue)
                    )

                    st.caption(
                        f"Estimated revenue over "
                        f"{horizon} days."
                    )

            with i2:

                with st.container(border=True):

                    st.metric(
                        "PEAK FORECAST",
                        money(peak_value)
                    )

                    st.caption(
                        "Highest projected daily revenue."
                    )

                    st.write(
                        peak_row["ds"].strftime(
                            "%d %b %Y"
                        )
                    )

            with i3:

                with st.container(border=True):

                    st.metric(
                        "LOWEST DAILY FORECAST",
                        money(lowest_value)
                    )

                    st.caption(
                        "Lowest projected daily revenue."
                    )

            st.write("")

            # -----------------------------------------------
            # MODEL PERFORMANCE
            # -----------------------------------------------

            left, right = st.columns(2)

            with left:

                with st.container(border=True):

                    st.subheader(
                        "Model Performance"
                    )

                    m1, m2 = st.columns(2)

                    with m1:

                        st.metric(
                            "MAE",
                            f"{mae:,.2f}"
                        )

                    with m2:

                        st.metric(
                            "RMSE",
                            f"{rmse:,.2f}"
                        )

                    st.caption(
                        "In-sample historical model-fit metrics."
                    )

            with right:

                with st.container(border=True):

                    st.subheader(
                        "Forecast Method"
                    )

                    st.write(
                        "Prophet Time-Series Model"
                    )

                    st.write(
                        "✓ Weekly seasonality"
                    )

                    st.write(
                        "✓ Yearly seasonality"
                    )

                    st.write(
                        "✓ Historical trend"
                    )

                    st.write(
                        "✓ Prediction interval"
                    )

            st.write("")

            # -----------------------------------------------
            # TABLE
            # -----------------------------------------------

            with st.container(border=True):

                st.subheader(
                    "Forecast Schedule"
                )

                forecast_table = (
                    future_forecast[
                        [
                            "ds",
                            "yhat",
                            "yhat_lower",
                            "yhat_upper"
                        ]
                    ]
                    .copy()
                )

                forecast_table.columns = [
                    "Date",
                    "Forecast",
                    "Lower Bound",
                    "Upper Bound"
                ]

                forecast_table["Date"] = (
                    forecast_table["Date"]
                    .dt.strftime("%d %b %Y")
                )

                for column in [
                    "Forecast",
                    "Lower Bound",
                    "Upper Bound"
                ]:

                    forecast_table[column] = (
                        forecast_table[column]
                        .round(2)
                    )

                st.dataframe(
                    forecast_table,
                    use_container_width=True,
                    hide_index=True
                )

                csv_data = (
                    forecast_table
                    .to_csv(index=False)
                )

                st.download_button(
                    "↓ Download Forecast CSV",
                    csv_data,
                    "NEXORA_Forecast.csv",
                    "text/csv"
                )

            st.success(
                f"✓ Forecast generated successfully "
                f"for the next {horizon} days."
            )

        except Exception as error:

            st.error(
                f"Forecast generation failed: {error}"
            )

# ============================================================
# BUSINESS INSIGHTS
# ============================================================

elif page == "Business Insights":

    st.subheader(
        "Business Insights"
    )

    st.caption(
        "Data-driven signals from your sales dataset."
    )

    st.write("")

    i1, i2, i3, i4 = st.columns(4)

    with i1:

        st.metric(
            "PROMO AVG",
            money(promo_avg)
        )

    with i2:

        st.metric(
            "NORMAL AVG",
            money(normal_avg)
        )

    with i3:

        st.metric(
            "PROMOTION LIFT",
            pct(promo_difference)
        )

    with i4:

        st.metric(
            "WEEKEND DIFFERENCE",
            pct(weekend_difference)
        )

    st.write("")

    left, right = st.columns(2)

    with left:

        with st.container(border=True):

            st.subheader(
                "Promotion Impact"
            )

            fig = go.Figure(
                go.Pie(
                    labels=[
                        "Promotion",
                        "Non-Promotion"
                    ],
                    values=[
                        promo_avg,
                        normal_avg
                    ],
                    hole=0.67,
                    textinfo="percent",
                    marker=dict(
                        colors=[
                            PURPLE,
                            "#DDD6FE"
                        ]
                    )
                )
            )

            fig.update_layout(
                height=400,
                template="plotly_white"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            if promo_difference >= 0:

                st.success(
                    f"Average revenue during promotions "
                    f"is {promo_difference:.1f}% higher "
                    f"than non-promotion transactions."
                )

            else:

                st.warning(
                    f"Average revenue during promotions "
                    f"is {abs(promo_difference):.1f}% lower "
                    f"than non-promotion transactions."
                )

    with right:

        with st.container(border=True):

            st.subheader(
                "Weekend vs Weekday"
            )

            fig = go.Figure(
                go.Pie(
                    labels=[
                        "Weekend",
                        "Weekday"
                    ],
                    values=[
                        weekend_avg,
                        weekday_avg
                    ],
                    hole=0.67,
                    textinfo="percent",
                    marker=dict(
                        colors=[
                            BLUE,
                            "#DBEAFE"
                        ]
                    )
                )
            )

            fig.update_layout(
                height=400,
                template="plotly_white"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            st.info(
                f"Weekend average revenue: "
                f"{money(weekend_avg)}"
            )

    st.write("")

    with st.container(border=True):

        st.subheader(
            "Revenue by Product"
        )

        product_chart = (
            product_revenue
            .reset_index()
        )

        fig = px.bar(
            product_chart,
            x="product",
            y="sales",
            text_auto=".2s"
        )

        fig.update_traces(
            marker_color=PURPLE,
            textposition="outside"
        )

        fig.update_layout(
            height=420,
            template="plotly_white",
            xaxis_title=None,
            yaxis_title="Revenue"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.write("")

    with st.container(border=True):

        st.subheader(
            "Key Observations"
        )

        st.markdown(
            f"""
            **01 — Product concentration**

            {top_product} generates the largest share of
            total revenue at approximately
            **{pct(top_product_share)}**.

            **02 — Promotion signal**

            Promotion transactions have an average revenue
            of approximately **{money(promo_avg)}**.

            **03 — Weekend signal**

            Weekend transactions have an average revenue
            of approximately **{money(weekend_avg)}**.

            **04 — Dataset coverage**

            NEXORA is analysing **{transactions:,} transactions**
            across the available historical period.
            """
        )

# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "NEXORA 2.0  •  Sales Intelligence & Demand Forecasting  •  "
    "Built with Streamlit + Plotly + Prophet"
)