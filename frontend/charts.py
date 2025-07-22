import matplotlib.pyplot as plt

# Plots a bar chart of total amount spent per vendor.
def plot_vendor_chart(df):
    # Group receipt amounts by vendor and compute total per vendor
    vendor_group = df.groupby("Vendor")["Amount"].sum()
    
    # Create bar chart for visualization
    fig, ax = plt.subplots(figsize=(10, 6))
    vendor_group.plot(kind="bar", ax=ax, color='skyblue', edgecolor='black')
    
    # Customize chart appearance
    ax.set_title("Total Spend by Vendor", fontsize=16, fontweight='bold')
    ax.set_xlabel("Vendor", fontsize=12)
    ax.set_ylabel("Amount (₹)", fontsize=12)
    ax.tick_params(axis='x', rotation=45)
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    return fig
