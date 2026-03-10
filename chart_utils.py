import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Modern color palette for professional dashboards
COLOR_PALETTE = {
    'primary': '#667eea',
    'secondary': '#764ba2',
    'accent': '#f093fb',
    'success': '#4CAF50',
    'warning': '#FF9800',
    'danger': '#F44336',
}

PLOTLY_TEMPLATE = "plotly_white"


def detect_chart_type(df: pd.DataFrame) -> str:
    """Decide which chart type best fits the dataframe.

    Rules:
    - categorical + numeric -> 'bar'
    - date + numeric -> 'line'
    - numeric only -> 'histogram'
    - small categorical distribution -> 'pie'
    - multiple numeric -> 'scatter' or 'box'

    The caller should handle cases where the determination is ambiguous.
    """
    if df.empty:
        return "none"

    # inspect columns
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    datetime_cols = df.select_dtypes(include=["datetime64", "datetime"]).columns.tolist()
    object_cols = df.select_dtypes(include="object").columns.tolist()

    # date + numeric -> line
    if datetime_cols and numeric_cols:
        return "line"

    # categorical + numeric -> bar (choose first of each)
    if object_cols and numeric_cols:
        return "bar"

    # numeric only -> histogram or box
    if numeric_cols and not object_cols and not datetime_cols:
        if len(numeric_cols) > 1:
            return "scatter"
        return "histogram"

    # small categorical -> pie
    if object_cols:
        # pick first object column and see unique count
        unique = df[object_cols[0]].nunique()
        if unique <= 10:
            return "pie"
        else:
            # default back to bar with counts
            return "bar"

    return "none"


def generate_chart(df: pd.DataFrame):
    """Return a professionally styled Plotly figure appropriate for the data frame."""
    chart_type = detect_chart_type(df)
    if chart_type == "none" or df.empty:
        return None

    try:
        if chart_type == "line":
            return _generate_line_chart(df)
        elif chart_type == "bar":
            return _generate_bar_chart(df)
        elif chart_type == "histogram":
            return _generate_histogram(df)
        elif chart_type == "pie":
            return _generate_pie_chart(df)
        elif chart_type == "scatter":
            return _generate_scatter_chart(df)
    except Exception:
        return None

    return None


def _generate_line_chart(df: pd.DataFrame):
    """Generate a professional line chart."""
    datetime_cols = df.select_dtypes(include=["datetime64", "datetime"]).columns.tolist()
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    
    if not datetime_cols or not numeric_cols:
        return None
    
    x = datetime_cols[0]
    y = numeric_cols[0]
    
    # Sort by date for better line visualization
    try:
        df_sorted = df.sort_values(by=x)
    except:
        df_sorted = df
    
    fig = px.line(
        df_sorted,
        x=x,
        y=y,
        title=f"{y} Trend Over {x}",
        labels={x: x.title(), y: y.title()},
        template=PLOTLY_TEMPLATE,
        markers=True
    )
    
    fig.update_traces(
        line=dict(color=COLOR_PALETTE['primary'], width=3),
        marker=dict(size=8, color=COLOR_PALETTE['primary'])
    )
    
    fig.update_layout(
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        height=400,
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    return fig


def _generate_bar_chart(df: pd.DataFrame):
    """Generate a professional bar chart."""
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    object_cols = df.select_dtypes(include="object").columns.tolist()
    
    if object_cols and numeric_cols:
        x = object_cols[0]
        y = numeric_cols[0]
        
        fig = px.bar(
            df,
            x=x,
            y=y,
            title=f"{y} by {x.title()}",
            labels={x: x.title(), y: y.title()},
            template=PLOTLY_TEMPLATE,
            color=y,
            color_continuous_scale="Viridis"
        )
    else:
        # Fallback: simple count bar
        col = object_cols[0] if object_cols else df.columns[0]
        value_counts = df[col].value_counts().reset_index()
        value_counts.columns = [col, "count"]
        
        fig = px.bar(
            value_counts,
            x=col,
            y='count',
            title=f"Distribution of {col.title()}",
            labels={col: col.title(), 'count': 'Count'},
            template=PLOTLY_TEMPLATE,
            color='count',
            color_continuous_scale="Blues"
        )
    
    fig.update_traces(
        marker=dict(line=dict(width=0))
    )
    
    fig.update_layout(
        hovermode='closest',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        height=400,
        margin=dict(l=50, r=50, t=80, b=50),
        xaxis_tickangle=-45 if len(df) > 10 else 0
    )
    
    return fig


def _generate_histogram(df: pd.DataFrame):
    """Generate a professional histogram for numeric data."""
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    
    if not numeric_cols:
        return None
    
    col = numeric_cols[0]
    
    fig = px.histogram(
        df,
        x=col,
        nbins=30,
        title=f"Distribution of {col.title()}",
        labels={col: col.title(), 'count': 'Frequency'},
        template=PLOTLY_TEMPLATE,
        color_discrete_sequence=[COLOR_PALETTE['primary']]
    )
    
    fig.update_traces(
        marker=dict(line=dict(color='white', width=1))
    )
    
    fig.update_layout(
        hovermode='x',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        height=400,
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    return fig


def _generate_pie_chart(df: pd.DataFrame):
    """Generate a professional pie chart."""
    object_cols = df.select_dtypes(include="object").columns.tolist()
    
    if not object_cols:
        return None
    
    col = object_cols[0]
    counts = df[col].value_counts().reset_index()
    counts.columns = [col, "count"]
    
    fig = px.pie(
        counts,
        names=col,
        values="count",
        title=f"Distribution of {col.title()}",
        template=PLOTLY_TEMPLATE,
        color_discrete_sequence=px.colors.sequential.Viridis
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>"
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        height=400,
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    return fig


def _generate_scatter_chart(df: pd.DataFrame):
    """Generate a scatter plot for multiple numeric columns."""
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    
    if len(numeric_cols) < 2:
        # Fallback to histogram if not enough numeric columns
        return _generate_histogram(df)
    
    x_col = numeric_cols[0]
    y_col = numeric_cols[1]
    color_col = numeric_cols[2] if len(numeric_cols) > 2 else None
    
    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        color=color_col,
        title=f"{y_col.title()} vs {x_col.title()}",
        labels={x_col: x_col.title(), y_col: y_col.title()},
        template=PLOTLY_TEMPLATE,
        color_continuous_scale="Viridis" if color_col else None,
        size_max=10
    )
    
    fig.update_traces(
        marker=dict(size=10, opacity=0.7, line=dict(width=0.5, color='white'))
    )
    
    fig.update_layout(
        hovermode='closest',
        plot_bgcolor='rgba(240,240,240,0.5)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        height=400,
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    return fig

