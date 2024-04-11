# OpenGovSalary

Building upon the good work of [lordidiot](https://github.com/lordidiot), the passage of time has unfortunately broken [his script](https://github.com/lordidiot/OpenGovSalary). This is my attempt at fixing it, alongside some cosmetic improvements. The full data obtained from OGP's API can be found [here](https://github.com/roycehoe/OpenGovSalary/blob/main/data.json), accurate as at 11/04/2024.

## Set-up

- Install [poetry](https://python-poetry.org/docs/1.3#installing-with-the-official-installer) on your machine
- Install all project dependencies with `poetry install`
- Activate the project virtual environment by running the command `poetry shell`
- Run the command `uvicorn main:app --reload` to start the backend server on your machine. The server should be running on localhost:8000
- Optional: To view the Swagger UI of this application, visit localhost:8000/docs
- Note that due to the number of API calls to OGP, it could take up to 30 seconds to a minute to receive a successful response from the API

## Sample output

Here is a sample output, generated from data available on 31082023.

| Name           | Title                                    | Annual Salary |
| -------------- | ---------------------------------------- | ------------- |
| Ivan           | Senior Software Engineer                 | $265,441      |
| Malcolm        | Software Engineer                        | $235,493      |
| Wee Loong      | Senior Software Engineer                 | $235,493      |
| Alwyn          | Senior Software Engineer                 | $224,928      |
| Foong Yi Zhuan | Senior Product Manager                   | $220,416      |
| Khant          | Senior Software Engineer                 | $220,416      |
| Christabel Png | Senior Product Designer                  | $220,416      |
| Yong Jie       | Senior Software Engineer                 | $220,416      |
| Si Han         | Software Engineer                        | $220,416      |
| Prakriti       | Software Engineer                        | $210,111      |
| Alexis         | Senior Software Engineer                 | $210,111      |
| Hena           | Product Manager                          | $208,337      |
| Le Yang        | Software Engineer                        | $204,245      |
| Kevan          | Senior Software Engineer                 | $204,245      |
| Wei Lun        | Software Engineer                        | $201,707      |
| Jie Hao        | Senior Software Engineer                 | $200,274      |
| Kok Seng       | Software Engineer                        | $200,274      |
| Prawira        | Senior Software Engineer                 | $200,274      |
| Sufyan         | Senior Product Designer                  | $200,274      |
| May Ying       | Senior Software Engineer                 | $198,824      |
| Yi Xin         | Lead Product Designer                    | $197,186      |
| Jennifer       | Product Manager                          | $196,113      |
| Khaleedah      | Product Designer                         | $196,113      |
| Reshma         | Product Manager                          | $194,435      |
| Pras           | Product Designer                         | $193,656      |
| Chinyao        | Software Engineer                        | $193,656      |
| Kendra         | Product Operations Specialist            | $193,656      |
| Zi Xiang       | Software Engineer                        | $193,656      |
| Kishen         | Software Engineer                        | $193,656      |
| Richard        | Senior Software Engineer                 | $193,656      |
| Hanu           | Lead Software Engineer                   | $193,656      |
| Jiayee         | Software Engineer                        | $193,656      |
| Amanda         | None                                     | $193,656      |
| Stanley        | Senior Software Engineer                 | $193,656      |
| Antariksh      | Senior Software Engineer                 | $191,106      |
| Zong Han       | Software Engineer                        | $191,106      |
| Kishore        | Software Engineer                        | $190,502      |
| Jia Chin       | Software Engineer                        | $190,502      |
| Qilu           | Lead Software Engineer                   | $190,502      |
| Se Hyun        | Product Designer                         | $190,502      |
| Jan            | Senior Product Manager                   | $190,502      |
| Zhong Jun      | Software Engineer                        | $190,502      |
| Harish         | Senior Software Engineer                 | $190,502      |
| Alex           | Senior Software Engineer                 | $190,502      |
| Feli           | Product Designer                         | $189,269      |
| Zeke           | Software Engineer                        | $189,269      |
| Jason          | Senior Software Engineer                 | $189,269      |
| Pete           | Senior Product Manager                   | $189,269      |
| Stacey         | Product Designer                         | $187,132      |
| Ken            | Senior Software Engineer                 | $187,132      |
| Wan Ling       | Software Engineer                        | $187,132      |
| Justyn         | Software Engineer                        | $187,132      |
| Kahhow         | Product Operations Specialist            | $184,780      |
| Jasmine        | Software Engineer                        | $184,780      |
| Hui Ling       | Software Engineer                        | $184,780      |
| Caleb          | Software Engineer                        | $184,780      |
| Jen Wei        | Software Engineer                        | $184,780      |
| Adan           | Lead Product Manager                     | $184,780      |
| Qimmy          | Senior Product Designer                  | $184,780      |
| Suhaila        | Senior Product Operations Specialist     | $180,198      |
| Kenneth Sng    | Senior Product Manager                   | $180,198      |
| Enyi           | Software Engineer                        | $180,198      |
| Cheryl         | Senior Manager                           | $180,198      |
| Angel          | Lead Software Engineer                   | $180,198      |
| Tiffany        | Product Designer                         | $180,198      |
| Nicholas       | Senior Software Engineer                 | $180,198      |
| Cheri          | Software Engineer                        | $180,198      |
| Moses          | Senior Product Manager                   | $178,455      |
| Fabian         | Software Engineer                        | $174,815      |
| Charmaine      | Senior Product Manager                   | $174,815      |
| Sean           | Software Engineer                        | $174,815      |
| Carina         | Senior Product Designer                  | $174,815      |
| Christabel N.  | Senior Software Engineer                 | $165,398      |
| Latasha        | Software Engineer                        | $162,083      |
| Rachel         | Senior Product Designer                  | $162,083      |
| Arshad         | Senior Software Engineer                 | $162,083      |
| Zi Yang        | Software Engineer                        | $162,083      |
| Jess           | Product Manager                          | $162,083      |
| Zi Wei         | Software Engineer                        | $160,440      |
| Ajay           | Product Operations Specialist            | $158,069      |
| Ian            | Lead Software Engineer                   | $156,996      |
| Sheikh         | Senior Software Engineer                 | $156,635      |
| Jie Yin        | Product Operations Specialist            | $156,635      |
| Chin Yang      | Senior Software Engineer                 | $156,635      |
| Wen Jia        | Product Designer                         | $150,040      |
| Gautam         | Software Engineer                        | $150,040      |
| Raisa          | Senior Software Engineer                 | $146,944      |
| Chi Fa         | None                                     | $144,672      |
| Shu Li         | Senior Software Engineer                 | $144,672      |
| Hui Qing       | Software Engineer                        | $144,672      |
| Airika         | Senior Manager                           | $129,923      |
| Paul           | Senior Product Manager                   | $129,104      |
| Hygin          | Assistant Director                       | $129,104      |
| Pallani        | Lead Software Engineer                   | $127,642      |
| Shazli         | Product Operations Specialist            | $127,001      |
| Amelia         | None                                     | $126,590      |
| Kenneth Chang  | Senior Product Operations Specialist     | $124,755      |
| Amit           | Product Manager                          | $124,755      |
| Sebastian      | Lead Software Engineer                   | $124,755      |
| Kaiwen         | Lead Software Engineer                   | $123,643      |
| Oliver         | Senior Software Engineer                 | $120,132      |
| Nicole         | Senior Manager (Marketing)               | $120,132      |
| Jackson        | Senior Product Operations Specialist     | $117,747      |
| Natalie        | Senior Product Designer                  | $95,251       |
| Tim            | Lead Software Engineer                   | $93,566       |
| Daryl          | Senior Software Engineer                 | $92,390       |
| Sonjia         | Senior Product Manager                   | $73,472       |
| Clement        | Product Operations Specialist            | $72,612       |
| Dat            | Lead Software Engineer                   | $70,037       |
| Si Mun         | Software Engineer                        | $68,263       |
| Samuel         | Head of Product Operations               | $65,371       |
| Shannen        | Senior Manager (Marketing)               | $64,552       |
| Fiona          | Senior UX Researcher                     | $64,552       |
| Shanty         | Senior UX Writer                         | $64,552       |
| Shawn          | Senior Manager (Policy & Transformation) | $61,593       |
| Jing Yi        | Senior Product Designer                  | $61,593       |
| Louiz          | Software Engineer                        | $61,593       |
