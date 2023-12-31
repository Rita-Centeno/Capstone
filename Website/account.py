import streamlit as st
from info_files.countries import hdi_dict
from firebase_admin import firestore, auth


def app():
    st.title('Welcome to :blue[Doc-IT-Right] :lab_coat:')

    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'useremail' not in st.session_state:
        st.session_state.useremail = ''

    def try_login():
        """
        Authenticate the user
        """
        try:
            user = auth.get_user_by_email(email)
            st.session_state.username = user.uid
            st.session_state.useremail = user.email
            
            st.session_state.signedout = True
            st.session_state.signout = True    
            
        except: 
            st.warning('Login Failed')

    def reset():
        """
        Reset the username and email when the user signs out
        """
        st.session_state.signout = False
        st.session_state.signedout = False   
        st.session_state.username = ''
        st.session_state.useremail = ''

        
    if "signedout" not in st.session_state:
        st.session_state["signedout"] = False
    if 'signout' not in st.session_state:
        st.session_state['signout'] = False    
        

    
    if not st.session_state["signedout"]: # only show if the state is False, hence the button has never been clicked
        choice = st.selectbox('Login/Signup',['Login','Sign up'])
        email = st.text_input('Email Address')
        password = st.text_input('Password',type='password', placeholder='At least 6 characters')
        

        if choice == 'Sign up':
            # Retreive the necessary user information for sign up
            username = st.text_input("Enter your unique username")

            st.divider()

            firstname = st.text_input('First Name')
            lastname = st.text_input('Last Name')
            age = st.number_input('Age', 0, None, None)

            nationality = st.selectbox('Nationality', hdi_dict.keys(), None, format_func=lambda hdi: hdi_dict.get(hdi))
            nationality = round(nationality, 3) if nationality is not None else None

            st.write('Number of people in your household:')
            col1, col2, col3 = st.columns(3)
            babies = col1.number_input('Babies', 0, None, None, placeholder='Until 4 years old')
            children = col2.number_input('Children', 0, None, None, placeholder='Between 5 and 17')
            adults = col3.number_input('Adults', 0, None, None, placeholder='18+ years old')

            insurance = st.toggle('Do you have health insurance?')
            noinsurance = 1 if not insurance else 0
            affiliation = st.toggle("Do you want the clinic's card for future benefits?")
            affiliation = 1 if affiliation else 0
            confirmation = st.checkbox('I declare that the information above is correct')

            if st.button('Create my account'):
                if nationality is not None and babies is not None and children is not None and adults is not None and confirmation:
                    user = auth.create_user(email = email, password = password, uid=username)
                    
                    # Initialize the database
                    if 'db' not in st.session_state:
                        st.session_state.db = ''

                    db=firestore.client()
                    st.session_state.db=db

                    # Create the user's document
                    data={'Username':username,
                          'FirstName': firstname,
                          'LastName': lastname,
                          'Age':age,
                          'Email':email,
                          'WeekendConsults':0,
                          'WeekdayConsults':0,
                          'Adults':adults,
                          'Children':children,
                          'Babies':babies,
                          'AffiliatedPatient':affiliation,
                          'PreviousAppointments':0,
                          'PreviousNoShows':0,
                          'LastMinutesLate':0,
                          'NoInsurance':noinsurance,
                          'ExtraExamsPerConsult':0,
                          'CountryofOriginHDI':nationality
                          }
                    db.collection('Patients').document(username).set(data)
                
                    st.success('Account created successfully!')
                    st.markdown('Please Login using your email and password')
                    st.balloons()
                else:
                    st.warning('Please fill all the fields and confirm the information')
        else:
            st.button('Login', on_click=try_login)
            
            
    if st.session_state.signout:
        st.text('Name: ' + st.session_state.username)
        st.text('Email id: ' + st.session_state.useremail)
        st.button('Sign out', on_click=reset)