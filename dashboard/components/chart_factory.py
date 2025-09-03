import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

class ChartFactory:
    """Factory for creating standardized charts"""
    
    # Color palette
    COLORS = {
        'primary': '#6c5ce7',
        'secondary': '#fd79a8',
        'success': '#00b894',
        'warning': '#fdcb6e',
        'danger': '#e17055',
        'info': '#74b9ff',
        'light': '#ddd',
        'dark': '#2d3436'
    }
    
    @classmethod
    def create_trend_chart(cls, df, x_col, y_col, title, show_trend=True):
        """Create a trend line chart with optional trend line"""
        fig = go.Figure()
        
        # Main line
        fig.add_trace(go.Scatter(
            x=df[x_col],
            y=df[y_col],
            mode='lines+markers',
            name=title,
            line=dict(color=cls.COLORS['primary'], width=3),
            marker=dict(size=8, color=cls.COLORS['primary'])
        ))
        
        # Add trend line if requested
        if show_trend and len(df) > 1:
            z = np.polyfit(range(len(df)), df[y_col], 1)
            p = np.poly1d(z)
            fig.add_trace(go.Scatter(
                x=df[x_col],
                y=p(range(len(df))),
                mode='lines',
                name='Trend',
                line=dict(color=cls.COLORS['secondary'], width=2, dash='dash'),
                opacity=0.7
            ))
        
        fig.update_layout(
            title=title,
            xaxis_title=x_col.replace('_', ' ').title(),
            yaxis_title=y_col.replace('_', ' ').title(),
            hovermode='x unified',
            height=400,
            template='plotly_white'
        )
        
        return fig
    
    @classmethod
    def create_cohort_heatmap(cls, df, cohort_col, period_col, value_col, title):
        """Create a cohort retention heatmap"""
        pivot_df = df.pivot(index=cohort_col, columns=period_col, values=value_col)
        
        fig = go.Figure(data=go.Heatmap(
            z=pivot_df.values,
            x=[f"Week {col}" for col in pivot_df.columns],
            y=[str(idx)[:10] for idx in pivot_df.index],
            colorscale='RdYlBu_r',
            text=pivot_df.values,
            texttemplate="%{text:.1f}%",
            textfont={"size": 10},
            hoverongaps=False,
            colorbar=dict(title="Retention %")
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Weeks After Signup",
            yaxis_title="Signup Week",
            height=400,
            template='plotly_white'
        )
        
        return fig
    
    @classmethod
    def create_funnel_chart(cls, stages, values, title):
        """Create a conversion funnel chart"""
        fig = go.Figure(go.Funnel(
            y=stages,
            x=values,
            texttemplate='%{label}: %{value:,}<br>(%{percentInitial})',
            textfont_size=12,
            marker_color=[cls.COLORS['info'], cls.COLORS['primary'], 
                         cls.COLORS['secondary'], cls.COLORS['success']]
        ))
        
        fig.update_layout(
            title=title,
            height=400,
            template='plotly_white'
        )
        
        return fig
    
    @classmethod
    def create_segmentation_chart(cls, df, segment_col, metric_col, title):
        """Create a segmentation bar chart"""
        fig = px.bar(
            df, 
            x=segment_col, 
            y=metric_col,
            title=title,
            color=segment_col,
            color_discrete_sequence=list(cls.COLORS.values())
        )
        
        fig.update_layout(
            height=400,
            template='plotly_white',
            showlegend=False
        )
        
        return fig