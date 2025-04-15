import os

def update_script_save_path(script_path, output_filename):
    """Update the script to save the plot in static/plots directory."""
    with open(script_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Define the new output path
    new_output_path = os.path.join("static", "plots", output_filename)
    
    # Replace the previous filename in the script
    updated_content = content.replace("pyo.plot(fig, filename=\"", f"pyo.plot(fig, filename=\"{new_output_path}")
    
    # Write back the modified script
    with open(script_path, 'w', encoding='utf-8') as file:
        file.write(updated_content)
    
    print(f"Updated {script_path} to save plots in static/plots.")

# Update each script
update_script_save_path("C:/Users/HP/Desktop/Finance-Tracker/backend/bar_plot.py", "barplot.html")
update_script_save_path("C:/Users/HP/Desktop/Finance-Tracker/backend/heatmap.py", "heatmap.html")
update_script_save_path("C:/Users/HP/Desktop/Finance-Tracker/backend/linechart.py", "line_chart.html")
update_script_save_path("C:/Users/HP/Desktop/Finance-Tracker/backend/pie_chart.py", "pie_chart.html")
