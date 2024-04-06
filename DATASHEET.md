# DATASET OVERVIEW

## BASICS: CONTACT, DISTRIBUTION, ACCESS

1. Dataset name: NORMAN Police Department Incident Summary
2. Dataset version number or date: 2024-04-05
3. Dataset owner/manager contact information, including name and email:
    - Name: Bhagyaraj Varadaraju
    - Email: bhagyaraj.varadaraju@gmail.com, varadaraju.b@ufl.edu
4. Who can access this dataset (e.g., team only, internal to the company, external to the
company)?:
    - This is for public access.
5. How can the dataset be accessed?
    - The dataset can be accessed by running the program using the following command: **_pipenv run python assignment2.py --urls files.csv_**

## DATASET CONTENTS

6. What are the contents of this dataset? Please include enough detail that someone unfamiliar
with the dataset who might want to use it can understand what is in the dataset.
- What does each item/data point represent (e.g., a document, a photo, a person, a
country)?
    - This dataset contains the incident summaries of the Norman Police Department.
- How many items are in the dataset?
    - The dataset contains the items extracted from the given list of incident summary pdf files.
- What data is available about each item (e.g., if the item is a person, available data
might include age, gender, device usage, etc.)? Is it raw data (e.g., unprocessed text or
images) or features (variables)?
    - The dataset contains the following columns:
        - Day of the Week
        - Time of Day
        - Weather
        - Location Rank
        - Side of Town
        - Incident Rank
        - Nature
        - EMSSTAT
- For static datasets: What timeframe does the dataset cover (e.g., tweets from January
2010–December 2020)?
    - The dataset covers the incident summaries of the Norman Police Department from the given list of pdf files where each pdf file corresponds to a single date.

## INTENDED & INAPPROPRIATE USES

7. What are the intended purposes for this dataset?
    - The intended purpose of this dataset is to provide the incident summaries of the Norman Police Department by augmenting it for analysis and research purposes.
8. What are some tasks/purposes that this dataset is not appropriate for?
    - This dataset is not appropriate for any illegal activities or any activities that might harm the reputation of the Norman Police Department.

# DETAILS

## DATA COLLECTION PROCEDURES

9. How was the data collected?
- Describe data collection procedures and instruments.
    - The data was created by fetching the incident summary pdf files from the Norman Police Department website using the given URLs.
- Describe who collected the data (e.g., contractors).
    - The data was collected by fetching the pdfs from the list of urls given as input.
10. Describe considerations taken for responsible and ethical data collection (e.g., procedures, use
of crowd workers, recruitment, compensation).
    - The data was collected by fetching the pdfs from the list of urls given as input. The data was collected responsibly and ethically by not using any crowd workers or any other means of data collection.
11. Describe procedures and include language used for getting explicit consent for data collection
and use, and/or revoking consent (e.g., for future uses or for certain uses). If explicit consent
was not secured, describe procedures and include language used for notifying people about
data collection and use.
    - The data was collected from the Norman Police Department website which is publicly available. There was no explicit consent required for data collection.

## REPRESENTATIVENESS

12. How representative is this dataset? What population(s), contexts (e.g., scripted vs.
conversational speech), conditions (e.g., lighting for images) is it representative of?
    - The dataset is representative of the incident summaries of the Norman Police Department on the given dates. The dataset is not representative of any specific population or context.

    How was representativeness ensured or validated?
    - This is not applicable to this dataset as it is a collection of incident summaries.

    What are known limits to this dataset’s representativeness?
    - The dataset is limited to the incident summaries of the Norman Police Department on the given dates.
13. What demographic groups (e.g., gender, race, age, etc.) are identified in the dataset, if any?
    - The dataset does not contain any demographic groups as it is a collection of incident summaries.

    How were these demographic groups identified (e.g., self-identified, inferred)?
    - The dataset does not contain any demographic groups as it is a collection of incident summaries.

    What is the breakdown of the dataset across demographic groups? Consider also reporting
    intersectional groups (e.g., race x gender) and including proportions, counts, means or other
    relevant summary statistics.
    - The dataset does not contain any demographic groups as it is a collection of incident summaries.

Note: This information can help a user of this dataset understand what groups are represented in
the dataset. This has implications for the performance of models trained on the dataset and on its
appropriateness for fairness evaluations – e.g., comparisons of performance across groups.

## DATA QUALITY

14. Is there any missing information in the dataset? If yes, please explain what information is
missing and why (e.g., some people did not report their gender).
Note: Consider the impact of missing information on appropriate uses of this dataset.
    - The dataset contains few missing information in the weather and side of the town columns. This is because few of the incident locations were not converted to (lat, lon) by the geopy library.
15. What errors, sources of noise, or redundancies are important for dataset users to be aware of?
    - The dataset contains few errors in the side of the town columns. This is because of the calculation of the orientation of the incident location by the geographiclib library.
16. What data might be out of date or no longer available (e.g., broken links in old tweets)?
    - The data might be out of date or no longer available if the Norman Police Department website removes the incident summary pdf files.
17. How was the data validated/verified?
    - The data was validated by checking the extracted data from the pdf files and comparing it with the actual pdf files before augmenting and creating the new dataset. We also wrote unit tests to validate the functionality of the pipeline.
18. What are potential validity issues a user of this dataset needs to be aware of (e.g., survey
answers might not be truthful, age was guessed by a model and might be incorrect, GPA was
used to quantify intelligence)?
    - The dataset contains few missing information in the weather and side of the town columns. This is because few of the incident locations were not converted to (lat, lon) by the geopy library. The dataset contains few errors in the side of the town columns. This is because of the calculation of the orientation of the incident location by the geographiclib library.
19. What are other potential data quality issues a user of this dataset needs to be aware of?
    - The dataset contains few missing information in the weather and side of the town columns. This is because few of the incident locations were not converted to (lat, lon) by the geopy library. The dataset contains few errors in the side of the town columns. This is because of the calculation of the orientation of the incident location by the geographiclib library.

## PRE-PROCESSING, CLEANING, AND LABELING

20. What pre-processing, cleaning, and/or labeling was done on this dataset?
Include information such as: how labels were obtained, treatment of missing values, grouping
data into categories (e.g., was gender treated as a binary variable?), dropping data points.
    - The data was pre-processed by extracting the incident summaries from the pdf files and converting them into a list of lists. The data was cleaned by removing the unwanted characters and converting the incident related data into a list of lists. The data was labeled by creating a SQLite database with a table called 'incidents' with the following columns: incident_time, incident_number, incident_location, nature, incident_ori. Then it was augmented to created a new dataset with the following columns: Day of the Week, Time of Day, Weather, Location Rank, Side of Town, Incident Rank, Nature, EMSSTAT.

    Who did the pre-processing, cleaning, and/or labeling (e.g., were crowd workers involved in
    labeling?)
    Note: Consider how this might impact appropriate users of this dataset (e.g., binary gender might
    be insufficient for fairness evaluations; imputing missing values with the mean may create
    anomalies in models trained on the data).
    - The pre-processing, cleaning, and labeling was done by the program written by me using the given list of incident summary pdf files. There were no crowd workers involved in labeling.
21. Provide a link to the code used to preprocess/clean/label the data, if available.
    - https://github.com/bhagyaraj-varadaraju/cis6930sp24-assignment2
22. If there are any recommended data splits (e.g., training, development/validation, testing),
please explain.
    - The recommended data split is 60:20:20 for training, validation, and testing respectively. This is to ensure that the model is trained on a larger dataset and validated on a smaller dataset to avoid overfitting.

## PRIVACY

23. What are potential data confidentiality issues a user of this dataset needs to be aware of?
    - There are no potential data confidentiality issues in this dataset as the base dataset is publicly available.

    How might a dataset user protect data confidentiality?
    - The dataset user can protect data confidentiality by not sharing the dataset with any unauthorized users and by not using the dataset for any illegal activities.
24. Is it possible to identify individuals (i.e., one or more natural persons), either directly or
indirectly (i.e., in combination with other data) from the dataset?
    - No, it is not possible to identify individuals from this dataset as there are no personal information in the dataset.

    Does the dataset contain data that might be considered sensitive in any way (e.g., data that
    reveals race, sexual orientation, age, ethnicity, disability status, political orientation, religious
    beliefs, union memberships; location; financial or health data; biometric or genetic data;
    criminal history)?
    - No, the dataset does not contain any sensitive information.

If the answer to either of these questions is yes, please be sure to consult with a privacy expert
and receive approvals for storing, using, or distributing this dataset.

25. If an analysis of the potential impact of the dataset and its uses on data subjects (e.g., a data
protection impact analysis) exists, please provide a brief description of the analysis and its
outcomes here and include a link to any supporting documentation.
    - There is no analysis of the potential impact of the dataset and its uses on data subjects as the dataset does not contain any personal information.

26. If the dataset has undergone any other privacy reviews or other relevant reviews (legal,
security) please include the determinations of these reviews, including any limits on dataset
usage or distribution.
    - The dataset has not undergone any privacy reviews or other relevant reviews as the dataset does not contain any personal information.

## ADDITIONAL DETAILS ON DISTRIBUTION & ACCESS

27. How can dataset users receive information if this dataset is updated (e.g., corrections,
additions, removals)?
Note: Consider creating a distribution list people can subscribe to.
    - The dataset users can receive information if this dataset is updated by subscribing to the repository where the dataset is hosted.
28. For static datasets: What will happen to older versions of the dataset? Will they continue to be
maintained?
    - The older versions of the dataset will continue to be maintained and will be available for access as long as the base dataset is available for those dates.
29. For streaming datasets: If this dataset pulls telemetry data from other sources, please specify:
- What sources
- How frequently the dataset is refreshed
Aether Data Documentation Template 6
- Who controls access to these sources
- Whether access to these sources will remain available, and for how long
- Any applicable access restrictions to these sources including licenses and fees
- Any other available access points to these sources
- Any relevant information about versioning
Are there any other ways in which these sources might affect this dataset that a dataset user
needs to be aware of?
    - This dataset does not pull telemetry data from other sources as it is not a streaming dataset.
30. If this dataset links to data from other sources (e.g., this dataset includes links to content such
as social media posts or, news articles, but not the actual content), please specify:
- What sources
- Whether access to these sources will remain available, and for how long
- Who controls access to these sources
- Any applicable access restrictions to these sources including licenses and fees
- For static datasets: If an official archival version of the complete dataset exists (i.e.,
including the content as it was at the time the dataset was created), where it can be
accessed
Are there any other ways in which these sources might affect this dataset that a dataset user
needs to be aware of?
    - This dataset does not link to data from other sources as it does not contain any links to social media posts or news articles.

31. Describe any applicable intellectual property (IP) licenses, copyright, fees, terms of use, export
controls, or other regulatory restrictions that apply to this dataset or individual data points.
These might include access restrictions related to data subjects’ consenting or being notified of
data collection and use, as well as revoking consent.
Provide links to or copies of any such applicable terms.
    - The dataset is publicly available and does not contain any intellectual property (IP) licenses, copyright, fees, terms of use, export controls, or other regulatory restrictions.
