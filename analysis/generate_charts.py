"""Generate charts for the prompt-wars README."""

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.size'] = 12

# Resolve paths relative to this script so it works from any directory
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_ROOT_DIR = os.path.dirname(_SCRIPT_DIR)
ASSETS = os.path.join(_ROOT_DIR, "assets")

def load_data():
    df = pd.read_csv(os.path.join(_ROOT_DIR, "results", "strategy_scores.csv"))
    # Extract version number for sorting
    df['v_num'] = df['version'].str.extract(r'v(\d+)').astype(float)
    df = df.sort_values('v_num')
    return df

def chart_evolution(df):
    """Strategy evolution chart — the hero image."""
    fig, ax = plt.subplots(figsize=(14, 6))

    # Color by phase
    phase_colors = {
        'thresholds': '#6B7280',
        'minimal': '#6B7280',
        'compliance': '#3B82F6',
        'psychology': '#8B5CF6',
        'math': '#EF4444',
        'simplify': '#6B7280',
        'conditional': '#EF4444',
        'breakthrough': '#F59E0B',
        'propose-back': '#10B981',
        'accept': '#F59E0B',
        'efficient': '#EF4444',
        'hold': '#6B7280',
        'mirror': '#EF4444',
        'aggressive': '#EF4444',
    }

    colors = [phase_colors.get(p, '#6B7280') for p in df['phase']]

    ax.bar(range(len(df)), df['local_avg'] * 100, color=colors, width=0.8, alpha=0.85)

    # Highlight key milestones
    milestones = {
        'v15': 'Compliance\ntriggers',
        'v62': '"Never\nconcede"',
        'v65': 'Propose-\nback',
        'v81': 'Zero\nguard',
    }

    for i, row in df.iterrows():
        idx = df.index.get_loc(i)
        if row['version'] in milestones:
            ax.annotate(
                milestones[row['version']],
                xy=(idx, row['local_avg'] * 100 + 1),
                ha='center', va='bottom',
                fontsize=9, fontweight='bold',
                color='#1F2937',
            )

    # Styling
    ax.set_ylabel('Score (%)', fontsize=13, fontweight='bold')
    ax.set_xlabel('Strategy Version', fontsize=13, fontweight='bold')
    ax.set_title('81 Prompt Strategies Tested: The Evolution', fontsize=16, fontweight='bold', pad=15)
    ax.set_ylim(30, 95)
    ax.axhline(y=55.3, color='#EF4444', linestyle='--', alpha=0.4, label='Baseline (v1)')
    ax.axhline(y=84.2, color='#10B981', linestyle='--', alpha=0.4, label='Best (v81)')
    ax.legend(loc='upper left', fontsize=10)
    ax.set_xticks(range(0, len(df), 5))
    ax.set_xticklabels([df.iloc[i]['version'] if i < len(df) else '' for i in range(0, len(df), 5)], rotation=45, ha='right', fontsize=8)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"{ASSETS}/evolution-chart.png", dpi=150, bbox_inches='tight', facecolor='white')
    print("Saved evolution-chart.png")

def chart_ambiguity(df):
    """Ambiguity vs precision comparison — the key finding."""
    fig, ax = plt.subplots(figsize=(10, 5))

    strategies = [
        ('v65\n"Propose it back\nto them"', 85.5, '#10B981'),
        ('v73\n"You can have\nALL [THIRD]"', 70.5, '#F59E0B'),
        ('v75\n"Take exactly what\nthey offered you"', 38.6, '#EF4444'),
    ]

    names = [s[0] for s in strategies]
    scores = [s[1] for s in strategies]
    colors = [s[2] for s in strategies]

    bars = ax.barh(names, scores, color=colors, height=0.6, alpha=0.9)

    for bar, score in zip(bars, scores):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                f'{score}%', va='center', fontsize=14, fontweight='bold')

    ax.set_xlim(0, 100)
    ax.set_title('Ambiguity Beats Precision', fontsize=16, fontweight='bold', pad=15)
    ax.set_xlabel('Average Score (%)', fontsize=13, fontweight='bold')
    ax.invert_yaxis()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='x', alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"{ASSETS}/ambiguity-chart.png", dpi=150, bbox_inches='tight', facecolor='white')
    print("Saved ambiguity-chart.png")

def chart_phases(df):
    """Phase comparison showing what worked and what didn't."""
    fig, ax = plt.subplots(figsize=(10, 5))

    phases = [
        ('Thresholds & Math\n(v1-v10)', 61.5, '#6B7280'),
        ('Compliance Triggers\n(v12-v20)', 66.0, '#3B82F6'),
        ('Psychology & Simplify\n(v21-v61)', 63.5, '#8B5CF6'),
        ('Conditional Logic\n(v63-v64, v79)', 64.0, '#EF4444'),
        ('"Never Concede"\n(v62)', 79.8, '#F59E0B'),
        ('Propose-Back\n(v65)', 85.5, '#10B981'),
        ('Zero Guard\n(v81)', 84.2, '#059669'),
    ]

    names = [p[0] for p in phases]
    scores = [p[1] for p in phases]
    colors = [p[2] for p in phases]

    bars = ax.barh(names, scores, color=colors, height=0.6, alpha=0.9)

    for bar, score in zip(bars, scores):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                f'{score}%', va='center', fontsize=12, fontweight='bold')

    ax.set_xlim(0, 100)
    ax.set_title('What Worked vs What Failed', fontsize=16, fontweight='bold', pad=15)
    ax.set_xlabel('Average Score (%)', fontsize=13, fontweight='bold')
    ax.invert_yaxis()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='x', alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"{ASSETS}/phases-chart.png", dpi=150, bbox_inches='tight', facecolor='white')
    print("Saved phases-chart.png")

if __name__ == "__main__":
    df = load_data()
    chart_evolution(df)
    chart_ambiguity(df)
    chart_phases(df)
    print("\nAll charts generated in assets/")
