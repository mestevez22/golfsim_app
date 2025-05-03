import pandas as pd 

#filter data 
def filter_data(data, date_range, selected_club):
    filtered = data[data['Date'].between(pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1]))]

    if isinstance(selected_club, list):
        if 'All' in selected_club and len(selected_club) == 1:
            pass  
        else:
            filtered = filtered[filtered['Club'].isin(selected_club)]
    else:
        if selected_club != 'All':
            filtered = filtered[filtered['Club'] == selected_club]

    return filtered
