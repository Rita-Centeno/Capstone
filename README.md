# Doc-IT-Right - Capstone Project 👨‍⚕️
#### Fall Semester 2023/2024

### Table of contents

1. [Project Description](#proj_desc)
1.1 [Main Technologies Used](#main_tech)
1.2 [Main Challenges Faced](#main_chal)
2. [Repository Description](#rep_desc)
3. [How to Use](#proj_use)
4. [Credits](#credits)
5. [License](#license)
6. [References](#ref)

<a name="proj_desc"></a>
## Project Description

Our project comes in the sense of a university course - Capstone Project - on our final year of a Bachelor's Degree in Data Science at Nova IMS.

Our fictional company, Doc-IT-Right,  is part of the consultancy sector. However, it falls under the health sector, as it intends to provide a solution for the scheduling and management of appointments in different medical specialties of a medical clinic. 

Our project aims to develop an interface that allows the management of a medical office, including a website with information about the company (https://docitrightcp.wixsite.com/doc-it-right) and also a chatbot that will directly interact with the patient, clarifying all of its doubts. In addition, a predictive model was also developed to predict which appointments were more likely to be missed by patients; therefore, empowering the clinics to better manage their schedules (possibly contacting the patient as a reminder of the appointment or confirming if it is still coming).

Our mission is to guarantee that clinics can deliver the best possible service to their patients, in the most effective way possible. This software will open up the possibility of increasing the quality of medical service with less or equal resources. By effectively organizing data, doctors and other collaborators can dedicate their time to other more complex and important actions, that will benefit patients in a great way, instead of spending time with routine, basic and repetitive actions that can be performed by this software.

This way, and in a country where there is such a great qualified labour but not so much quantity of it, we aim to get the best out of the available workforce, challenging them into new, more rewarding tasks, and manage them into success and contentment of patients that can, in this way, have better medical care and see their doubts quickly resolved.

<a name="main_tech"></a>
### - What main technologies were used in the development of this project?
For this project, the main goal was to create an AI-powered Question Answer System which would engage with fictional customers - in our case patients of medical clinics. This would be the primary communication channel of our business - being able to offer services to customers (answering patient's medical specialities, as well as their medication doubts; giving the predictions of which appointments are more likely to be missed to clinics) through a conversational app. 

With this project, we were able to explore more in-depth how to make use of LLM models, from OpenAI, in different problems (with Python being the chosen programming language) -through the development of a chatbot that is able to perform appointment scheduling actions, solve patient doubts and predict which appointments are more likely to be missed - as well as we learned how to create an applications using streamlit and a website on WIX.

<a name="main_chal"></a>
### - What were the main challenges faced? 
The main challenges faced during the development of this project were related with:
- Team's limited budget in OpenAi - using and interacting with the chat. Hence, there was a need to become more cautious and restrict some of the parts of the development stage;
- The chatbot required very specific instructions to ensure the right outputs, which was an extremely time-consuming process (sort of trial and error).
- There was not enough time to predict and consequently code all the possible human-generated inputs. However, that is something that can be improved with time and user help and reviews.

<a name="rep_desc"></a>
## Repository Description
This repository contains all the files created during the development of our project. In the following paragraphs will be a description of how the repository is organized and what each file contains:
- [Prompts folder](Prompts): contains all the links that lead to the chats where the prompts were fed into the LLM (in our case, ChatGPT) to obtain - company definition (company name, problem, value proposition, core values, mission, vision, tag line, personas), marketing prompts (discussion of pros and cons of reviews from competitor companies, blog posts creation, pitch script, 5-post social media campaign, Instagram post captions), timetable scheduling prompt and patient data generator prompt.
- [No Show Prediction](No_show_prediction): this is a folder that contains both a Jupyter notebook containing the development of a predictive model for no-show appointments and another Jupyter notebook where the data needed for this task are properly treated.
- [Website](Website): this folder contains all the needed files for the chatbot application, on streamlit, to work properly.
- [Requirements](requirements.txt): file that specifies the dependencies and the versions that need to be installed in the environment for the project to run.
- [Use Cases](use_cases.pdf): this file contains practical examples of scenarios in which our chatbot appication can be helpful to clients of our company - appointment scheduling, appointment rescheduling, appointment cancellations, clarifying medical doubts, predictive model.
- [Data Description](data_description.txt): this text file contains the description and the metadata of all the used data in our project.
- [Git Ignore](.gitignore): this file specifies patterns of files and directories that should be excluded from the version control of our repository.
- [README](README.md): file that contains the basic instructions of how to run the project, the motivations behind it and its features.
- [LICENSE](LICENSE.md): this is a file that contains the chosen license for this project.

##
<a name="proj_use"></a>
## How To Use the Project
Divided into two parts: informative website on WIX (https://docitrightcp.wixsite.com/doc-it-right) and the streamlit app (which also has the link for the other website).

##
### How to Install and Run the Project

tirar o código github / clone repository
descarregar pasta com credenciais (API), dados usados..mudar path no ficheiro .env
dentro da pasta no-show prediction, there is a need for changing the path in the ...
dar run nos requirements

to run the project:
inside the terminal there is a need to open the website folder
`streamlit run main.py`

After this you can have fun interacting with our Dr.Chatbot 🥳.

<a name="credits"></a>
## 
#### Project Developed by:
- Bruna Faria | 20211529@novaims.unl.pt  
- Catarina Oliveira | 20211616@novaims.unl.pt  
- Inês Vieira | 20211589@novaims.unl.pt 
- Joana Rosa | 20211516@novaims.unl.pt  
- Rita Centeno | 20211579@novaims.unl.pt
##

<a name="license"></a>
## License
This project is licensed under the [GNU AGPLv3] - see the [LICENSE.md](LICENSE.md) file for details.
##

<a name="ref"></a>
## References
Here are some of the most important contents our team checked during the development of the project:
- OpenAI. (2023). ChatGPT (Jan 7 version) [Large language model](https://chat.openai.com/chat)
- [Streamlit Components](https://streamlit.io/components?category=widgets)
- [Additional Streamlit Components](https://docs.streamlit.io/library/api-reference/widgets/st.multiselect)
- [How to deploy the application](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app)
- [Schedule Chatbot Option](https://www.pragnakalp.com/how-to-use-openai-function-calling-to-create-appointment-booking-chatbot/)
- [Chatbot Langchain Memory](https://stackoverflow.com/questions/76240871/how-do-i-add-memory-to-retrievalqa-from-chain-type-or-how-do-i-add-a-custom-pr)
