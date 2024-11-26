# Finance Tracking App (Django)

## Features Overview

### 1. **Plaid API Integration**

- Successfully integrated the Plaid API with support for fetching transactions.
- Custom sandbox user (`custom_nuraly`) is used for testing purposes.
- Fetched transactions are dynamically displayed on the dashboard.
- API keys and environment variables are securely managed using `.env`.

### 2. **Interactive Dashboard**

- **Plotly Integration**:
  - A dynamic dashboard provides interactive visualizations of user transactions.
  - Supports filtering by month.
  - Includes:
    - A bar chart to display transaction amounts by name.
    - A pie chart showing the top 5 highest expenses for the selected month.
- Transactions are displayed in a table, dynamically updated based on user-selected filters.

### 3. **Dynamic ERD Creation**

- Utilized `django-extensions` and `graphviz` to dynamically generate an Entity-Relationship Diagram (ERD) for the project.
- Command:

     ```bash or zsh
     ./manage.py graph_models -a > my_project.dot
     ./manage.py graph_models -a | dot -Tpng -o my_project_ERD.png
     ```

- Output:
  - `.dot` file for further customizations.
  - `.png` file for quick visualization.
- **Interactive Preview**: Use the [Graphviz Interactive Preview](https://marketplace.visualstudio.com/items?itemName=EFanZh.graphviz-preview) VS Code extension for better `.dot` file visualization.
