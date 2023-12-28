import streamlit as st

from streamlit_option_menu import option_menu


import chat, account, schedule, about
st.set_page_config(
        page_title="Doc-IT-Right",
)



class MultiApp:

    # def __init__(self):
    #     self.apps = []

    # def add_app(self, title, func):

    #     self.apps.append({
    #         "title": title,
    #         "function": func
    #     })

    def run():
        # app = st.sidebar(
        with st.sidebar:        
            app = option_menu(
                menu_title='Doc-IT-Right',
                options=['Chat','Account','Schedules','about'],
                icons=['chat-fill','person-circle','calendar-week-fill','info-circle-fill'],
                menu_icon='check-circle-fill',
                default_index=1,
                styles={
                    "container": {"padding": "5!important","background-color":'black'},
        "icon": {"color": "white", "font-size": "23px"}, 
        "nav-link": {"color":"white","font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "blue"},
        "nav-link-selected": {"background-color": "#02ab21"},}
                
                )

        
        if app == "Chat":
            chat.app()
        if app == "Account":
            account.app()          
        if app == 'Schedules':
            schedule.app()
        if app == 'about':
            about.app()    
             
          
             
    run()            