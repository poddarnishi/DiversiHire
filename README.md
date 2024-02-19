## Inspiration
Rethinking Recruitment Through Equihire
HackHer's keynote speaker ignited a powerful conversation within our team, prompting us to confront the pervasive issue of bias in our industry's hiring practices. We recognize the insidious nature of unconscious bias, where deeply ingrained beliefs and societal conditioning can unfairly disadvantage diverse candidates. Despite legal advancements and evolving social attitudes, a disturbing reality persists qualified individuals from underrepresented groups still face significant hurdles in securing employment.
As highlighted by studies, applicants of color must navigate a system where they are consistently required to submit significantly more applications compared to their white counterparts to secure even a single interview opportunity. This stark disparity, extending beyond race to encompass gender and other identities, underscores the urgent need for transformative solutions.

In response to this critical challenge, we introduce Equihire, a revolutionary blind recruitment platform. This innovative approach goes beyond masking personal data like age, gender, and education. Equihire takes the unprecedented step of **anonymizing voices during interviews**, ensuring that candidates are evaluated solely on their skills and qualifications, free from the influence of personal biases.

## What it does
Equihire goes beyond anonymizing resumes. We leverage the power of Named Entity Recognition (NER) with spaCy to identify and neutralize potential markers of identity like race, age, gender, and religion within applicants' resumes. This empowers candidates to craft a level playing field for themselves, showcasing their skills and qualifications without the influence of personal background.
Equihire offers a comprehensive suite of features to facilitate fair and unbiased hiring:
1.  Initial Screening Transparency: Integrate Equihire seamlessly into your initial screening process, ensuring anonymity and transparency from the outset.
2.  Unbiased Assessment: Focus solely on candidate responses and qualifications, eliminating the influence of bias in the evaluation process.
3.  Blind Pre-screening Interviews: Conduct video interviews where the system transcribes the conversation and presents the audio in a uniform voice, removing any identifying characteristics.
4.  Seamless Candidate Experience: Provide a user-friendly and engaging interview experience for all candidates, fostering a positive first impression.

Applicant Journey:
1. Onboarding: Applicants seamlessly join Equihire using their Google account or creating a new profile.
2. Dashboard Access: The intuitive dashboard provides an overview of relevant job opportunities and platform features.
3. Job Search: Applicants can leverage search filters to find suitable positions and submit anonymized applications with a single click.
4. Resume Upload: Resumes are uploaded and automatically anonymized, removing any potential identifiers.
5. Video Interviews: Shortlisted candidates participate in video interviews where their responses are transcribed and voices are masked, ensuring unbiased evaluation.

Recruiter Journey:
1. Job Creation: Recruiters effortlessly create new job listings, detailing requirements and specifics for each role.
2. Applicant Review: Anonymized applications and resumes allow recruiters to assess candidates solely based on their qualifications and skills.
3. Interview Management: Schedule interviews, access masked audio recordings from interviews, and communicate effectively with candidates through the platform.

## How we built it:
Front-end: HTML, CSS, Javascript, Bootstrap
Middleware & Backend: Python, Flask, SQLAlchemy
ML Stack: PDF Parser, SpaCy, Speech Recognition, Setence-Bert, Named Entity Recognition, GTTS

## Challenges we ran into
The challenges we encountered included difficulty in resume sanitization, making it challenging to determine what to include. Additionally, integrating all the components within a tight timeframe proved to be another hurdle. Furthermore, finding a model that accurately compared job descriptions with interview answers for applicants was also a significant challenge.

## Accomplishments that we're proud of
We're thrilled to have completed this project on time despite a tight deadline due to prior commitments. We managed to implement most of the envisioned features, and the late-night coding sessions definitely added to the team spirit! This project stands out from our usual hackathons due to its unique nature. The in-depth brainstorming and research phase led to a fulfilling sense of accomplishment upon successful completion.

## What we learned
This project was a whirlwind of learning and collaboration, pushing us to new heights in software engineering. We not only mastered the intricacies of GitHub and honed our time management skills under pressure, but also delved into the fascinating world of cutting-edge technologies like Named Entity Recognition (NER) and Speech Recognition.

## What's next for EquiHire
   1. We plan to leverage artificial intelligence and machine learning algorithms  to more accurately identify and neutralize implicit bias triggers in resumes and interviews, including subtle cues that may currently escape detection. 
 2.⁠ ⁠We aim to develop predictive analytics tools to help organizations understand and improve their diversity hiring metrics over time.
 3.⁠ ⁠Equihire aims to extend its reach to support organizations and job seekers worldwide. This includes localizing our platform to accommodate various languages and cultural contexts, making blind recruitment a global standard.


## Youtube link
https://www.youtube.com/watch?v=zQujn0Dww7E&t=1s
