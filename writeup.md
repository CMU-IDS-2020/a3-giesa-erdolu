# Tracing the Presidential Debate 2020. 

![A screenshot of your application. Could be a GIF.](presDebSS.png)


1- Goals of the project

1.1 Aim

The interest in our project was to trace and reveal the dynamics of a conversation through data visualization. We explored the potential of visualization to capture and represent converstaional dynamics.
 
1.2 Site and Data                                                                                                                                                              Our site was the first “Presidential Debate of the 2020 Elections” that took place on September 19th 2020 between President Donald J. Trump and former Vice President and Presidential candidate Joe Biden. The debate was moderated by journalist and television anchor Chris Wallace. We refer to them as “actors” in this project. We worked with a transcript of the debate that allowed us to do text processing on a corpus of the debate conversation. Text processing allowed us to extract and visualize various dimensions of the conversation.

1.3 Question                                                                                                                                                                     The question that we explored in the project, and that the prototype we built in response, was twofold.

Part 1- First, we were interested in tracing the trajectory of the conversation between the actors. We were interested in the weight and speech attitude of the actors throughout the conversation. The questions we looked at were:
   - What was the weight of each actor in terms of their presence in the conversation? What were the moments in the debate where the conversation was between the   
     candidates? How long were these moments? What were the moments of intervention by the moderator?
   - Which actor spoke the most? If we take that as part of “weight”, how did that weight develop for each actor throughout the conversation? Which actor interrupted the 
     others the most? If we take that as part of “attitude”, how did that attitude follow throughout the conversation? Which actor’s speech was broken by crosstalks the 
     most?
 
Part 2- Secondly, we were interested in tracing the weight of themes / topics, and their distribution throughout the conversation. We were interested in investigating the weight that each actor put on the themes / topics in the conversation. We were also interested in the weights of actors in pointing to themselves and pointing fingers to others. The questions we looked at were:
   - What were the weights of themes / topics in the conversation? What were the windows in the conversation in which they were discussed? How long were those windows?
   - What were the weights that each candidate put on the themes? Which thematic words were emphasized more within each theme / topic and across the themes / topics? What were 
     the thematic words emphasized more by each candidate and what was the weight of that emphasis by a candidate compared to the other?
   - What were the weights that each candidate put in pointing to themselves and pointing fingers to others? 
 
We believe these questions point to important dynamics in a presidential debate that are significant matters of discussion within the political realm and media, and that essentially affect mass perception. So, we aim to shed light on these dimensions by visualizing the conversation.  
 
To investigate these questions, we identified a list of dimensions to search and visualize within the debate conversation. These dimensions are described in the “Design Process” section. Essentially, this required extracting our own data -related to these dimensions- from the transcript of the debate. So, the prototype we built included text processing, data extraction and framing, and visualization. 
 
1.4 Framework
For text processing, data extraction, and data framing, we used NLTK (a language processing library for Python) and pandas (a data analysis library for Python). For data visualization, we used Streamlit (an open source app framework) and Altair (a data visualization library for Python).  
 

2- Design Process

2.1 Qualitative Evaluation of the Conversation                                                                                                                                The initial step was going over the transcript. A careful reading and qualitative evaluation of the text allowed us to identify the dimensions of the conversation we wanted to search in investigating the questions. This step also involved sketching and brainstorming on the preliminary design ideas on the ways these dimensions could potentially be visualized.
 
Workflow
(Emek + Katherine) 
 
This step was a collaborative effort by both members. Combined with step 2, this step took about a quarter of the work time.
 
2.2 Identifying the Dimensions of Conversation 
To investigate the questions in Part 1, we defined:
   - Actor-Time: This dimension shows who was speaking at a particular moment in the conversation and patterns of interaction between the moderator and candidates (moments of 
     intervention) as well as between the candidates (moments of debate). It also shows the length of these patterns. 
   - Number of Words-Time: This dimension shows an incremental count of words by each actor on a particular moment in the conversation. It shows who had spoken the most up to a 
     certain moment in the conversation. It also shows how the weight of each actor changed throughout the conversation.
   - Number of Words-Order of Speech: This dimension shows an incremental count of words by each actor over the course of the conversation. It shows who had spoken the most up 
     to a certain order of speech (order count of turns of speech e.g. fifty fourth turn) in the conversation. It also shows how the weight of each actor changed throughout the      conversation.
   - Number of Interruptions-Time: This dimension shows an incremental count of interruptions* made by each actor over the course of the conversation. It also shows the 
     moments of interruptions by each actor. It provides hints about this particular speech attitude of each actor within a period or throughout the entire conversation. 
     *Interruptions were marked with ‘—’ in the transcript.
   - Number of Interruptions-Order of Speech: This dimension shows an incremental count of interruptions by each actor over the course of the conversation. It shows who had 
     interrupted the most up to a certain order of speech in the conversation. It also shows how this number changed for each actor throughout the conversation.
   - Number of Crosstalks-Time: This dimension shows an incremental count of crosstalks* during an actor’s speech over the course of the conversation. It also shows the moments 
     of crosstalk. It provides hints about how this particular speech attitude occurred within a period or throughout the entire conversation. 
     *Interruptions were marked as “[crosstalk hh:mm:ss]” in the transcript.
   - Number of Crosstalks-Order of Speech: This dimension shows an incremental count of crosstalks during an actor’s speech over the course of the conversation. It shows 
     whose speeches were broken by the crosstalks the most up to a certain order of speech in the conversation. It also shows how this number changed for each actor throughout 
     the conversation.
 
All these dimensions involve a temporality to show the aspect (e.g. actor, number of words, etc.) within a moment or period in the conversation as well as through the overall conversation. Based on that, more refined ideas were discussed and produced for the visualizations of these dimensions. 
 
To investigate the questions in Part 2, we outlined:
   - the 6 themes that the debate conversation included: healthcare, covid, economy, environment, race, and election. These themes were generally set by Chris Wallace. Using 
     these themes, we qualitatively selected frequently used, or key thematic words associated with the broad theme. For example, 'mask' and 'vaccine' were two of the key 
     words related to covid. 
   - a list of thematic words under each time that are used in the conversation*
   *This was by our qualitative evaluation of the debate transcript.
 
Based on the themes, we defined:
   - Number of Healthcare-Time:  This dimension shows an incremental count of words related to healthcare by each actor on a particular moment in the conversation. It shows the 
   weight that actors put on healthcare up to a certain moment in the conversation. It also shows how the weight that each actor put on healthcare changed throughout the 
   conversation.
   - Number of Healthcare-Order of Speech: This dimension shows an incremental count of words related to healthcare by each actor over the course of the conversation. It shows 
   the weight that actors put on healthcare up to a certain order of speech in the conversation. It also shows how the weight that each actor put on healthcare changed 
   throughout the conversation. It also shows the windows in the conversation in which healthcare was discussed as well as the length of that window.
 
The dimensions below show the same information described for healthcare the other 5 themes.
   - Number of Covid - Order of Speech
   - Number of Economy - Time
   - Number of Economy - Order of Speech
   - Number of Environment - Time
   - Number of Environment - Order of Speech
   - Number of Race - Time
   - Number of Race - Order of Speech
   - Number of Election - Time
   - Number of Election - Order of Speech
 
   - Word Count-Theme: This dimension shows a total count of words related to a particular theme by each actor. It shows the weight that actors put on each theme in the 
     conversation and the weight of the theme in the conversation overall.
   - Word Count-Actor-Word: This dimension shows a total count of each thematic word used by each actor. It shows the emphasis that actors put on each thematic word and thereby 
     the theme in the conversation. 
   - Word Count-Actor-Pointing to Self and Fingers to Others: This dimension shows a total count of “Pointing to Self and Fingers to Others” (PSFO) words (“you” “he” and “I”) 
     used by each actor. It shows the weight of pointing to self and pointing fingers to others by each actor in the conversation.  
 
as the dimensions to be extracted as data by processing the conversation text and to be visualized for insights. All these dimensions involve the notion of “thematic weight” within a period in the conversation as well as through the overall conversation. More refined ideas were discussed and produced for the visualizations of these dimensions.
 
Workflow
(Emek + Katherine) 
 
This step was a collaborative effort by both members. Combined with step 1, this step took about a quarter of total work time.
 
2.3 Text Processing, Data Extraction, and Data Framing
From here, we began processing the conversation text to extract the identified dimensions. These dimensions became the categories in the data that constituted the two data frames that were used in creating the visualizations. These data frames were carefully discussed between the team members and created according to the ways the intended visualizations required. 
 
The first data frame contains the data ordered by Order of Speech and Time. It was structured as follows: 
   - df1 = {Order of Speech: [], Actor: [], Time: [], Number of Words: [], Number of Interruptions: [], Number of Crosstalks: [], Number of Number Use: [], Number of 
     Healthcare: [], Number of Covid: [], Number of Environment: [], Number of Election: [], Number of Economy: [], Number of Race: []} 
 
The second data frame is ordered by the Theme Words. It was structured as follows: 
   - df2 = {Theme Word: [], Broad Theme: [], Actor: [], Word Count: []}
 
Workflow
(Emek) 
Part of the code that extracts the data on the dimensions in Part 1.
 
(Emek + Katherine) 
Part of the code that extracts the data on themes over time (in Part 2). Combined with the first part of the code, this part created the first data frame.
 
(Katherine) 
Part of the code that extracts the data on the rest of dimensions in Part 2. This part of the code created the second data frame.
 
Overall, this step involved coordinative and divided work. It took approximately half of the total work time.

2.4 Creating Interactive Data Visualizations 
Based on the dimensions and two data frames, we produced two sets of visualizations for the application: “Through the debate” set and “Thematic weights within the debate” set.
 
a- Through the debate
 
Visualizations:
   - Mini-map bar chart → Mini-map + (Actor-Number of Words-Time) 
   - Zoomable line chart → (Number of Words-Order of Speech) 
 
   - Mini-map bar chart → Mini-map + (Actor-Number of Interruptions-Time) 
   - Zoomable line chart → (Number of Interruptions-Order of Speech)
 
   - Mini-map bar chart → Mini-map + (Actor-Number of Crosstalks-Time)
   - Zoomable line chart → (Number of Crosstalks-Order of Speech)
 
Minimap bar charts were designed to allow a user to traverse the debate to see the dimensions in Part 1. The user can do it in two ways: (1) By brushing over a mini-map of the debate to create a time frame and moving it (2) By using the “Order of Speech” slider and sliding between the n(th) orders of speech. 
 
Each minimap bar chart was made of a set of charts:
   - A mini-map: A map of the debate that allows the user to create a time frame by brushing and travel through the matrix chart and bar chart by moving the frame.
   - A matrix chart: A chart that maps Actor (on Y axis) on Time (on X axis hidden*) with color coded squares that represent Actor. It shows patterns of intervention by the 
     moderator, and patterns and lengths of debate between the candidates. The matrix chart can be navigated through the mini-map or slider which is in sync with the bar chart.
   - A bar chart: A chart that maps Number of “something” (e.g. Number of Words, Number of Interruptions, etc.) (on Y axis) on Time (on X axis) with color coded bars that 
     represent Number of “something” and Actor. It shows the incremental counts and allows to compare them across the actors on a moment, within an interval, or throughout the      conversation. The bar chart can also be navigated through the mini-map or slider which is in sync with the matrix chart. It also has a tooltip interaction that shows the 
     Actor and Number of Words on each bar.
     *The matrix chart and bar chart were aligned and they both use the bar chart’s X axis that shows time. 
 
We chose these interactions because we wanted the user to be able to:
   - navigate through the timeline of the conversation (by mini-map or slider)
   - focus on a moment or a timeframe (by brushing on the mini-map or slider)
   - make comparisons by looking at the positions (such as Actor squares) or size of things (such as bars next to each other)
     check details (counts by tooltips, if necessary)
 
Each minimap bar chart was followed by:
   - A zoomable line chart: A line chart that maps Number of “something” (e.g. Number of Words, Number of Interruptions, etc.) (on Y axis) on Order of Speech (on X axis) with 
     color coded lines that represent Number of “something” and Actor. It shows trajectories of counts by each actor in relation to each other and throughout the conversation. 
     It also allows the user to compare them on a moment, within an interval, or throughout the conversation. The line chart can be navigated by zooming in / out and panning to 
     move forward or backward along the Order of Speech*. It can also be navigated by the slider. It also has a tooltip interaction that shows the Number of Words along the 
     line by each Order of Speech.
     *Order of Speech is essentially linked to Time as each Order of Speech is time stamped. However, different than Time, Order of Speech indicates how many turns of speech  
     preceded the current. For example, Order of Speech = 335 means the debate has passed 334 turns of speech by different actors. The 335th turn was by Joe Biden and it   
     started on 41:41. 
 
We chose these interactions because we wanted the user to be able to:
   - see an overall trajectory at a glance 
   - make comparisons by seeing the trajectory lines next to each other
   - check details (by zooming in, or counts by tooltips, if necessary)
   - navigate through the conversation (by panning or slider)
   - focus on a particular turn or a range of turns
 
b- Thematic weights within the debate
 
Visualizations:
Mini-map bar chart → Minimap + (Actor - Number of Healthcare - Time)
Zoomable line chart → (Number of Healthcare - Order of Speech) 
 
Mini-map bar chart → Minimap + (Actor - Number of Covid- Time) 
Zoomable line chart → (Number of Covid - Order of Speech)
 
Mini-map bar chart → Minimap + (Actor - Number of Economy - Time) 
Zoomable line chart → (Number of Economy - Order of Speech)
 
Mini-map bar chart → Minimap + (Actor - Number of Environment - Time) 
Zoomable line chart → (Number of Environment - Order of Speech)
 
Mini-map bar chart → Minimap + (Actor - Number of Race - Time) 
Zoomable line chart → (Number of Race - Order of Speech)
 
Mini-map bar chart → Minimap + (Actor - Number of Election - Time) 
Zoomable line chart → (Number of Election - Order of Speech)
 
Linked bar chart → Word Count - Theme
Linked bar chart → Word Count - Actor - Theme Words
 
Bar chart  →  Word Count - Actor - Pointing to self and others
 
 
Each minimap bar chart and zoomable line chart was designed in exactly the same ways described above. We chose these interactions for the same reasons described above.
 
The linked bar charts we designed was made of:
A bar chart: A chart that maps Word Count (on Y axis) on Theme (on X axis) with color coded bars that represent Word Count and Actor. It shows the total counts of theme words for each theme (both by Biden and Trump) by stacking the bars. It allows the user to compare the weight of themes in the overall conversation. It also allows the user to compare the weight of themes between the actors by comparing the size of stacked bars. The chart also has a tooltip interaction that shows the Actor on each bar. Each bar that is mapped to a theme can also be selected by clicking. This selection makes the second linked bar show a breakdown of the counts into theme words by each actor.
A bar chart: A chart that is linked to the first one, and that maps Word Count (on Y axis) on Actor (on X axis) and Theme Words (on column) with color coded bars that represent Word Count and Actor under each Theme Word. It shows the total count of each theme word by Actor. It also shows the weight of theme words within each theme. It also allows the user to compare the emphasis of theme words across the actors by comparing the size of bars. The chart also has a tooltip interaction that shows the Word Count on each bar. 
 
For example, clicking on the bar that indicates the “Covid” theme Word Count, will allow the user to see a side by side comparison of the “Covid” theme word (“vaccine”, “mask”, “death”, “dying”, “covid”) counts by each actor. 
 
We chose these interactions because we wanted the user to be able to:
see various layers of information in two charts
see overall by default and breakdowns by selection
make comparisons of counts, weights, and emphasis by counts and size of things (such as bars stacked or next to each other)
check details (counts by tooltips, if necessary)
 
The bar chart we designed:
A bar chart: A chart that maps Word Count (on Y axis) on Actor (on X axis) and “Pointing to Self and Fingers to Others” (PSFO) words (“You”, “He”, “I”) (on column) with color coded bars that represent Word Count and Actor under each PSFO word. It shows the total count of each PSFO word by Actor. It also allows the user to compare the emphasis of PSFO words across the actors by comparing the size of bars. The chart has a selection option with click that highlights PSFO Word Count by actor. The chart also has a tooltip interaction that shows the Word Count on each bar. 
 
We chose these interactions because we wanted the user to be able to:
see overall by default and breakdowns by selection
make comparisons of counts and emphasis by counts and size of things (such as bars next to each other)
check details (counts by tooltips, if necessary)
 
Workflow
(Emek) 
Part of the code that creates the visualizations of the “Through the debate” set. 
 
(Emek + Katherine) 
Part of the code that creates a part of the visualizations of the “Thematic weights within the debate” set (mini-map - bar chart - line chart combinations). 
 
(Katherine) 
Part of the code that creates the rest of the visualizations of the “Thematic weights within the debate” set (linked bar chart - bar chart combinations). 
 
Overall, this step involved coordinative and divided work. It took about a quarter of the total work time.
