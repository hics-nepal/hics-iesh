DATA = {
    'id': 'data',
    'title': 'Data & Technology',
    'icon': '📊',
    'color': '#bc8cff',
    'tagline': 'Numbers, patterns and systems — data literacy for the 21st century',
    'description': (
        'Every reading this device produces is a piece of data. But data without understanding '
        'is just noise. This module develops the skills to read, analyse, visualise and '
        'communicate with data — and explores the technology behind the device itself, '
        'from sensors to databases to the web. These are skills for every discipline, '
        'not just science.'
    ),
    'sensors': ['air_temp', 'air_hum', 'pressure', 'soil_temp', 'soil_moist', 'mq7_raw', 'mq135_raw'],
    'teaching_guide': (
        'The data literacy activities in this module are best approached as cross-curricular — '
        'the mathematics teacher, the ICT teacher and the English teacher all have stakes in '
        'these skills. The dashboard is the primary tool: encourage students to interact with '
        'it directly, change time ranges on charts, and form hypotheses before reading answers. '
        'The "How Does This System Work?" activity is excellent for students interested in '
        'engineering or computing — but frame the technical explanation as a story '
        '(a number\'s journey from the real world to your screen) rather than a list of '
        'components. The undergraduate research activity should be genuinely rigorous '
        '— if students produce something publishable, encourage them to submit it.'
    ),
    'activities': [

        {
            'id': 'data-01',
            'title': 'Numbers Tell Stories',
            'subtitle': 'Reading, interpreting and narrating what the dashboard shows',
            'grade_band': '6–8',
            'subjects': ['Mathematics', 'English'],
            'duration': '30 min',
            'type': 'observation',
            'viz_type': 'data-bars',
            'viz_config': {
                'title': 'All sensors at a glance — what story do these numbers tell together?',
                'sensors': [
                    {'key': 'air_temp',   'label': 'Air Temperature', 'unit': '°C',  'max': 45,   'color': '#3fb950'},
                    {'key': 'air_hum',    'label': 'Humidity',        'unit': '%',   'max': 100,  'color': '#58a6ff'},
                    {'key': 'soil_temp',  'label': 'Soil Temperature','unit': '°C',  'max': 45,   'color': '#d29922'},
                    {'key': 'soil_moist', 'label': 'Soil Moisture',   'unit': '%',   'max': 100,  'color': '#56d364'},
                    {'key': 'mq7_raw',    'label': 'CO (MQ-7)',       'unit': 'adc', 'max': 4095, 'color': '#f0883e'},
                    {'key': 'mq135_raw',  'label': 'Air Quality',     'unit': 'adc', 'max': 4095, 'color': '#f85149'},
                ],
                'note': 'The bar length shows how large each reading is relative to the sensor\'s maximum range.',
            },
            'overview': (
                'Students read the dashboard for the first time, identify the different types '
                'of information it displays, and practise translating numbers into plain-language '
                'descriptions — the foundational skill of data literacy.'
            ),
            'nepal_context': (
                'Nepal is producing more data about its environment than ever before — satellite '
                'imagery, weather station networks, agricultural surveys, health monitoring — '
                'but the ability to read and use this data is not evenly distributed. A student '
                'who can look at a chart, understand what it is measuring, spot a trend and '
                'write a clear sentence about what it means has a skill that is valuable in '
                'farming, public health, journalism, government and business. Data literacy '
                'is not a "tech skill" — it is a literacy.'
            ),
            'learning_objectives': [
                'Identify different types of data display (single value, bar, line chart) on the dashboard.',
                'Read specific values from charts and tables accurately.',
                'Describe a trend in a line chart using appropriate vocabulary (increasing, decreasing, stable, fluctuating).',
                'Write a short paragraph that accurately describes what the current sensor data shows.',
            ],
            'background': (
                'Data visualisation is the practice of representing numbers graphically so that '
                'patterns, trends and outliers become visible to the eye. A table of 100 numbers '
                'is hard to understand; the same numbers plotted as a line chart reveal whether '
                'something is rising, falling or stable at a glance. The dashboard you are '
                'looking at is a real-time data visualisation — it takes numbers from physical '
                'sensors and presents them in forms designed for quick human understanding.\n\n'
                'There are three basic types of data displayed: current values (single numbers '
                'updated continuously — the large numbers in each card), bar gauges (showing '
                'a percentage or proportion visually), and line charts (showing how values '
                'change over time). Each type answers a different question: "what is it now?", '
                '"how full/high is it?", and "how has it changed?".\n\n'
                'Describing data in words requires specific vocabulary. "The temperature '
                'increased" is vague. "The temperature increased by 3°C over two hours, '
                'from 22°C at 8am to 25°C at 10am" is precise and useful. Good data '
                'communication always includes: what changed, by how much, over what time '
                'period, and (if known) why.'
            ),
            'teacher_notes': (
                'Many students have never been asked to describe a graph in a complete sentence. '
                'Model it explicitly: point to the temperature chart and say aloud "I can see '
                'that the temperature was approximately X at Y time, and it has since increased '
                'by Z degrees — this might be because the sun has been heating the room since '
                'the morning." Then ask students to do the same for another chart. The writing '
                'task should be assessed on accuracy and clarity, not length.'
            ),
            'live_sensors': ['air_temp', 'air_hum', 'pressure', 'soil_moist'],
            'materials': ['Notebook', 'Pencil'],
            'procedure': [
                'Open the HICS dashboard. Spend 2 minutes just looking at it. What do you notice first?',
                'List all the different types of information displayed. How many different measurements are shown?',
                'Record 5 specific current values with their units. For example: "Air temperature = 24.3°C".',
                'Look at the temperature history chart. Describe the trend in one sentence: Is it going up, down, stable, or variable?',
                'Write a 3-sentence weather report describing current conditions at this station as if you were a radio weather presenter. Use all three values you recorded.',
                'Swap your weather report with a partner. Can they add any extra detail or correction from the same data?',
            ],
            'discussion_questions': [
                'Why is a line chart better than a table of numbers for understanding whether temperature is rising or falling?',
                'If a chart shows temperature rising sharply at one point, what might have caused it? List three possible explanations.',
                'What information is NOT shown on this dashboard that you wish you could see?',
            ],
            'worksheet_questions': [
                {
                    'q': 'Choose any one chart on the dashboard. Describe the trend you see in TWO sentences, using specific numbers and time references.',
                    'answer_guide': 'Should include: the name of the measurement, at least two specific values (not ranges), specific time references, and a trend description (increasing/decreasing/stable/fluctuating). Deduct marks for vague descriptions like "the temperature went up a bit".',
                    'marks': 4,
                },
                {
                    'q': 'Write a three-sentence "weather report" for this station using the current dashboard values. Include temperature, humidity, and one other measurement.',
                    'answer_guide': 'Award marks for accuracy (values match dashboard), correct units, and readable prose. The best answers will include interpretation (e.g. "The 65% humidity suggests moderate moisture in the air, consistent with current cloudy conditions.") not just repetition of numbers.',
                    'marks': 4,
                },
            ],
            'vocabulary': [
                {'term': 'Data Visualisation', 'definition': 'The representation of data in graphical or visual form to make patterns and trends easier to understand.'},
                {'term': 'Trend', 'definition': 'A general direction of change in data over time — upward, downward, stable or cyclical.'},
                {'term': 'Axis', 'definition': 'One of the two reference lines (horizontal x-axis, vertical y-axis) that define the coordinates of a graph.'},
                {'term': 'Real-Time Data', 'definition': 'Data that is collected, transmitted and displayed with minimal delay — showing what is happening now.'},
            ],
            'extension': (
                'Take one chart from the dashboard and export or sketch it. Add your own '
                'annotations: label the highest point, the lowest point, any unusual spikes, '
                'and write one sentence on the chart explaining what you think caused each '
                'notable feature.'
            ),
            'curriculum_link': 'Nepal CDC Grade 7 Mathematics, Unit 8: Data and Statistics; Grade 7 English, Unit 5: Descriptive Writing',
            'sdg_links': ['SDG 4: Quality Education', 'SDG 9: Industry, Innovation and Infrastructure'],
            'cross_curricular': [
                'Mathematics: Reading graphs, units, decimal numbers',
                'English: Descriptive writing, precise language, audience awareness',
                'ICT: Understanding dashboards and digital interfaces',
            ],
        },

        {
            'id': 'data-02',
            'title': 'Finding Patterns in Data',
            'subtitle': 'Statistics, correlation and the difference between pattern and proof',
            'grade_band': '8–10',
            'subjects': ['Mathematics', 'ICT', 'Science'],
            'duration': '45 min',
            'type': 'analysis',
            'overview': (
                'Students collect a multi-day dataset from the dashboard, calculate descriptive '
                'statistics, look for correlations between variables, and learn the crucial '
                'distinction between correlation and causation.'
            ),
            'nepal_context': (
                'Agricultural and climate decision-making in Nepal increasingly depends on '
                'the ability to spot patterns in environmental data — not just for individual '
                'farmers but for the district offices, NGOs and government agencies that '
                'design interventions. A data analyst who can look at a month of temperature '
                'and humidity records and identify an unusual trend is doing exactly the kind '
                'of work needed to protect Nepal\'s food security in a changing climate.'
            ),
            'learning_objectives': [
                'Calculate mean, median, mode and range for a real dataset.',
                'Construct a scatter plot from two variables and describe any apparent correlation.',
                'Explain the difference between correlation and causation with examples.',
                'Identify potential confounding variables that might explain an observed correlation.',
            ],
            'background': (
                'Descriptive statistics summarise a dataset with a small number of meaningful '
                'numbers. The mean (average) gives the central tendency; the range (maximum '
                'minus minimum) gives the spread; the standard deviation measures how much '
                'individual values deviate from the mean on average. Together these numbers '
                'give a compact description of what a dataset contains.\n\n'
                'A correlation is a statistical relationship between two variables — when one '
                'tends to be higher when the other is higher (positive correlation) or lower '
                '(negative correlation). For example, air temperature and humidity in Nepal '
                'tend to be positively correlated during monsoon season (both are high) but '
                'negatively correlated in winter (warm sunny days have low humidity). '
                'Correlations can be visualised as scatter plots and quantified with a '
                'correlation coefficient (r) from -1 to +1.\n\n'
                'The critical caution: correlation does not imply causation. Two variables '
                'can be correlated because one causes the other, because both are caused by '
                'a third variable, or simply by chance. Ice cream sales and drowning rates '
                'are correlated — not because ice cream causes drowning, but because both '
                'increase in summer (a confounding variable). In environmental science, '
                'claiming causation from correlation alone has led to expensive policy mistakes.'
            ),
            'teacher_notes': (
                'For the multi-day dataset, students can use the history charts on the dashboard. '
                'If the database has been running for several days, there will be real data to '
                'work with. If not, a week of readings taken by the class can be used. The '
                'correlation between air temperature and humidity is particularly interesting '
                '— it may be positive, negative or non-linear depending on the season, which '
                'itself teaches students that correlations can vary across contexts.'
            ),
            'live_sensors': ['air_temp', 'air_hum', 'soil_moist'],
            'materials': ['Graph paper or spreadsheet software', 'Calculator'],
            'procedure': [
                'Collect data: record air temperature and humidity for 10 time points from the history chart. Note the timestamps.',
                'Calculate: mean temperature, mean humidity, range for each. Show your working.',
                'Plot a scatter diagram: x-axis = temperature, y-axis = humidity. Each data point is one reading.',
                'Describe the correlation you see in the scatter plot: positive, negative, none, or non-linear?',
                'Calculate the ratio of each temperature reading to the corresponding humidity reading. Does this ratio stay constant, or does it vary?',
                'Hypothesis test: "Higher temperature causes higher humidity at this station." Is this supported by your data? What alternative explanation might explain the same pattern?',
            ],
            'discussion_questions': [
                'You find that soil moisture and air humidity are strongly correlated in your data. Does this prove that humid air causes wetter soil? What else might explain the correlation?',
                'A newspaper headline reads: "Scientists find link between humidity and crop yield." What would you need to know before believing that humidity causes yield changes?',
                'What additional data would you need to collect to test whether temperature causes humidity to change at this station, rather than both being caused by a third factor?',
            ],
            'worksheet_questions': [
                {
                    'q': 'From your 10 data points: calculate mean temperature (show working), mean humidity (show working), and the range for each variable.',
                    'answer_guide': 'Check arithmetic. Mean = sum ÷ 10. Range = max − min. Full marks for correct calculation and clear working shown.',
                    'marks': 6,
                },
                {
                    'q': 'Describe the correlation between temperature and humidity in your scatter plot. Is it positive, negative or absent? Give ONE alternative explanation for the pattern besides direct causation.',
                    'answer_guide': 'Correlation description should reference the scatter plot specifically (upward/downward/no trend). Alternative explanations: both driven by time of day (morning is cooler and more humid); both driven by weather system; both driven by monsoon season. Award marks for the quality of the alternative explanation.',
                    'marks': 4,
                },
                {
                    'q': 'Explain, using your own example, why correlation does not imply causation.',
                    'answer_guide': 'Award marks for a clear original example where two things correlate but neither causes the other (both caused by a third variable). Nepal examples: rice yield and rainfall are correlated but a drought year also causes other factors (low labour, low input use) that affect yield independently.',
                    'marks': 3,
                },
            ],
            'vocabulary': [
                {'term': 'Correlation', 'definition': 'A statistical relationship between two variables — when one tends to increase or decrease as the other does.'},
                {'term': 'Causation', 'definition': 'A relationship where one thing directly produces or influences another.'},
                {'term': 'Scatter Plot', 'definition': 'A graph where each point represents a pair of values from two variables, used to visualise correlations.'},
                {'term': 'Standard Deviation', 'definition': 'A measure of how spread out values in a dataset are from the mean — larger means more variability.'},
            ],
            'extension': (
                'Use spreadsheet software to calculate the Pearson correlation coefficient (r) '
                'for your temperature and humidity data. Interpret the result: what does an r '
                'of +0.7 or −0.4 tell you? Find the formula for r and understand each step.'
            ),
            'curriculum_link': 'Nepal CDC Grade 9 Mathematics, Unit 12: Statistics; Grade 9 ICT, Unit 4: Data Analysis',
            'sdg_links': ['SDG 4: Quality Education', 'SDG 2: Zero Hunger'],
            'cross_curricular': [
                'Mathematics: Statistics, graphs, correlation coefficient',
                'Science: Hypothesis testing, experimental design',
                'ICT: Spreadsheet analysis, data visualisation tools',
            ],
        },

        {
            'id': 'data-03',
            'title': 'How This System Works',
            'subtitle': 'Tracing a number\'s journey from the real world to your screen',
            'grade_band': '9–11',
            'subjects': ['ICT', 'Physics', 'Engineering'],
            'duration': '45 min',
            'type': 'experiment',
            'overview': (
                'Students trace the complete pathway of a single temperature reading — from '
                'the physical world, through the sensor, ADC, microcomputer, database and '
                'web server, to the browser — understanding how each step works and what '
                'can go wrong at each stage.'
            ),
            'nepal_context': (
                'Internet of Things (IoT) devices — sensors connected to networks and databases '
                '— are transforming how Nepal monitors its environment, agriculture and '
                'infrastructure. Nepal\'s hydropower stations use IoT sensors to monitor water '
                'levels. Agricultural projects use soil sensors to optimise irrigation. The '
                'technology in this device is the same technology, at small scale. Understanding '
                'how it works is foundational for anyone who wants to build, maintain or '
                'evaluate these systems in Nepal.'
            ),
            'learning_objectives': [
                'Describe the function of each hardware component in the sensor hub (sensor, ADC, microcomputer, database, web server).',
                'Explain the role of analogue-to-digital conversion in measuring physical quantities.',
                'Identify at least two places in the data pipeline where errors or noise could be introduced.',
                'Evaluate the concept of "the stack" as a framework for understanding complex systems.',
            ],
            'background': (
                'A sensor hub like this one consists of a layered "stack" of hardware and software, '
                'each layer serving a specific function. The physical sensors (BMP280, DHT22, '
                'DS18B20, MCP3208) measure physical phenomena and produce either analogue '
                'voltages or digital signals. Analogue sensors are connected to the MCP3208 '
                'ADC (analogue-to-digital converter), which samples the voltage at high speed '
                'and converts it to a 12-bit number (0–4095). Digital sensors communicate '
                'directly with the Raspberry Pi over I2C, SPI or 1-Wire protocols.\n\n'
                'The Raspberry Pi is a single-board computer running Linux. It runs Python '
                'code that reads from each sensor, logs readings to a SQLite database on its '
                'internal storage, and serves a Flask web application accessible over the '
                'local network. The web application reads data from the database and serves '
                'it as both an HTML dashboard and a JSON API at /api/data. When you open '
                'the dashboard on your device, your browser fetches the HTML once, then polls '
                'the /api/data endpoint every 15 seconds for updated readings.\n\n'
                'Each step in this pipeline can introduce errors. The sensor may have a '
                'calibration offset (the BMP280 temperature reading may be 1–2°C higher than '
                'actual due to self-heating). The ADC has quantisation noise — a 12-bit '
                'converter can represent 4,096 distinct levels; the real-world value falls '
                'somewhere between two of those levels. The database might have a write failure '
                'during a power cut. The web server might deliver a cached value rather than '
                'the latest reading. Understanding these failure modes is what separates a '
                'competent engineer from someone who just uses the hardware.'
            ),
            'teacher_notes': (
                'This activity is well suited to a hands-on approach: if possible, open the '
                'dashboard alongside the Raspberry Pi Python code (via SSH or a printed code '
                'listing). Show students what the Python code actually looks like — even at '
                'grade 9, seeing real code alongside the system that runs it is far more '
                'concrete than a diagram alone. The "trace a number" procedure is the '
                'pedagogical core: following one specific value end-to-end reveals the '
                'system architecture better than any lecture.'
            ),
            'live_sensors': ['air_temp', 'air_hum', 'pressure'],
            'materials': ['System architecture diagram (provided below)', 'Pencil for annotation'],
            'procedure': [
                'Read the current air temperature: ___ °C. This number has travelled a long path to reach your screen. You will trace it.',
                'Stage 1 — Sensor: The DHT22 sensor uses a capacitive element to measure humidity and a thermistor to measure temperature. It produces a digital signal, not an analogue voltage. Why does this mean it does NOT need the MCP3208 ADC?',
                'Stage 2 — Protocol: DHT22 sends data over a single GPIO pin using a proprietary timing protocol. The Raspberry Pi reads 40 bits: 16 bits temperature + 16 bits humidity + 8 bits checksum. What is a checksum and why is it useful?',
                'Stage 3 — Database: The reading is stored in a SQLite table called "telemetry" with columns for timestamp, temperature, humidity, etc. Write the SQL query that would retrieve the last 10 temperature readings.',
                'Stage 4 — API: The Flask web server has a route /api/latest that returns JSON. Write what you think the JSON response for the current temperature reading looks like.',
                'Stage 5 — Browser: JavaScript on the dashboard page fetches /api/latest every 15 seconds and updates the display. Identify one thing that could go wrong at this step and how the dashboard handles it.',
            ],
            'discussion_questions': [
                'The dashboard shows air temperature updating every 15 seconds, but the DHT22 sensor is read every 1 second. Why might there be a gap between reality and display?',
                'If the Raspberry Pi\'s clock is wrong (e.g. it has been disconnected from the internet for a month), how would this affect the timestamps in the database?',
                'If you wanted to scale this from one station to 100 stations across Nepal, what parts of the system would need to change? What parts could stay the same?',
            ],
            'worksheet_questions': [
                {
                    'q': 'Draw a simple block diagram showing the data flow from sensor to browser. Label each stage with its function.',
                    'answer_guide': 'Should include: Physical sensor → (ADC for analogue, direct for digital) → Raspberry Pi Python code → SQLite database → Flask web server → JSON API → Browser JavaScript → Display. Award marks for correct sequence and appropriate labels.',
                    'marks': 6,
                },
                {
                    'q': 'What is analogue-to-digital conversion? Why do the MQ gas sensors need an ADC but the DHT22 temperature sensor does not?',
                    'answer_guide': 'ADC converts a continuous analogue voltage to a discrete digital number. MQ sensors output an analogue voltage proportional to gas concentration — this must be digitised. DHT22 outputs a digital bit stream that the computer can read directly without conversion.',
                    'marks': 4,
                },
                {
                    'q': 'The MCP3208 is a 12-bit ADC. How many distinct values can it represent? If it is connected to a 3.3V reference, what is the smallest voltage change it can detect?',
                    'answer_guide': '2¹² = 4,096 distinct values (0–4095). Resolution = 3.3V ÷ 4,096 ≈ 0.000806V ≈ 0.8 mV. Award full marks for correct calculation and correct unit.',
                    'marks': 4,
                },
            ],
            'vocabulary': [
                {'term': 'ADC (Analogue-to-Digital Converter)', 'definition': 'A device that samples an analogue voltage at regular intervals and converts each sample to a digital number.'},
                {'term': 'Protocol', 'definition': 'An agreed set of rules for how data is formatted and transmitted between devices; I2C, SPI and 1-Wire are all communication protocols.'},
                {'term': 'API (Application Programming Interface)', 'definition': 'A defined way for software systems to communicate; the /api/data endpoint is an HTTP API that returns sensor data as JSON.'},
                {'term': 'Checksum', 'definition': 'A value calculated from a data transmission and sent alongside it; the receiver recalculates and compares to verify the data arrived intact.'},
            ],
            'extension': (
                'SSH into the Raspberry Pi and examine the Python code in core_dash.py. '
                'Identify: (1) where the DHT22 sensor is read, (2) where data is written '
                'to the database, (3) what happens if a sensor read fails. Write a one-page '
                'annotated code walkthrough explaining what each section does.'
            ),
            'curriculum_link': 'Nepal CDC Grade 10 ICT, Unit 5: Networks and Data; Grade 11 Computer Science, Unit 3: Systems Architecture',
            'sdg_links': ['SDG 4: Quality Education', 'SDG 9: Industry, Innovation and Infrastructure'],
            'cross_curricular': [
                'Physics: Analogue and digital signals, electrical circuits',
                'Mathematics: Binary numbers, resolution calculation',
                'ICT: Networks, databases, web architecture',
            ],
        },

        {
            'id': 'data-04',
            'title': 'Environmental Data Journalism',
            'subtitle': 'Turning sensor readings into stories that matter — and avoiding the traps',
            'grade_band': '11–12',
            'subjects': ['English', 'Media Studies', 'Social Studies'],
            'duration': '60 min',
            'type': 'project',
            'overview': (
                'Students analyse real sensor data, identify a newsworthy story within it, '
                'and produce a 400-word piece of environmental journalism — practising the '
                'skills of evidence-based writing, appropriate hedging and accurate claim-making.'
            ),
            'nepal_context': (
                'Nepal\'s media landscape is growing rapidly, but environmental journalism '
                'remains underdeveloped. Most reporting on climate change, air quality or '
                'agriculture either lacks data entirely or misrepresents statistical evidence. '
                'A journalist who understands what sensor data means — and, crucially, what '
                'it cannot mean — is a rare and valuable professional. This activity treats '
                'journalism as a data skill as much as a writing skill.'
            ),
            'learning_objectives': [
                'Identify a genuine newsworthy finding within a dataset.',
                'Write an accurate, evidence-based environmental news piece.',
                'Apply appropriate hedging language when making claims based on limited data.',
                'Recognise and avoid common data journalism errors (cherry-picking, misrepresenting correlation, ignoring context).',
            ],
            'background': (
                'Data journalism is the practice of building news stories from quantitative '
                'evidence. In environmental reporting, this means understanding what sensors '
                'measure, what the numbers mean in context, and what claims the data can and '
                'cannot support. The most common errors in environmental data journalism are: '
                'cherry-picking (choosing the time period that tells the most dramatic story), '
                'misrepresenting correlation as causation, presenting a single station\'s '
                'reading as representative of an entire region, and failing to include expert '
                'interpretation of unusual readings.\n\n'
                'Good environmental journalism uses several techniques. Primary source data '
                '(like this device\'s readings) is always more credible than second-hand '
                'summaries. Numbers need context — "CO reading of 350 raw ADC" means nothing '
                'to a reader; "CO levels 40% above this week\'s average, measured on a morning '
                'with burning crop residue nearby" is a story. Appropriate hedging language '
                '("readings suggest", "consistent with", "may indicate") is essential '
                'when data is limited or not fully calibrated.\n\n'
                'Nepal\'s Right to Information Act (2007) gives citizens the right to request '
                'environmental data held by government agencies. Environmental journalists '
                'who understand sensor data can use this right effectively to access, '
                'verify and report on government monitoring records.'
            ),
            'teacher_notes': (
                'The "find the story" part of this activity is genuinely challenging — '
                'encourage students to look at the data first and find something that '
                'surprises them, rather than deciding what story they want to tell and '
                'then looking for supporting data. The ethical boundary (do not cherry-pick) '
                'is the hardest lesson to internalise and the most important one. Peer '
                'review of draft articles is very effective: ask students to specifically '
                'look for unsupported claims in each other\'s writing.'
            ),
            'live_sensors': ['air_temp', 'air_hum', 'pressure', 'soil_moist', 'mq7_raw', 'mq135_raw'],
            'materials': ['Dashboard access', 'Writing materials'],
            'procedure': [
                'Spend 10 minutes exploring the full dashboard. Look at all charts, especially the history. Find one thing that genuinely surprises or interests you in the data.',
                'Write a "data note" — 3–4 bullet points describing what you found, using specific numbers and time references. No interpretation yet, just description.',
                'Now add context: research what was happening locally (weather, season, nearby activities) that might explain what you saw. Add this to your note.',
                'Write a 50-word headline and opening paragraph for a news story. The opening should answer: what happened, when, how much, and why it matters.',
                'Write the full 400-word article. Include: the specific data finding, context, one quote from a "source" (this can be a teacher playing a role, or a real published expert), and appropriate hedging where claims are uncertain.',
                'Read your article aloud and identify every claim. For each claim: is it directly supported by the data? If not, mark it for revision.',
            ],
            'discussion_questions': [
                'A journalist finds that temperature at this station has risen 2°C in the last week. Is this evidence of climate change? What would be the appropriate way to report it?',
                'What is the difference between saying "the data shows" and "the data suggests"? When should each be used?',
                'Nepal\'s Ministry of Environment holds air quality data for Kathmandu. Under what circumstances could a journalist request access to this data, and how might they use it?',
            ],
            'worksheet_questions': [
                {
                    'q': 'Write your 50-word headline and opening paragraph. Underline every specific data value you include.',
                    'answer_guide': 'Good opening paragraphs include: specific numbers with units; a time reference; something surprising or significant; accessible language for a general reader. Penalise vague openings that could apply to any environmental story.',
                    'marks': 5,
                },
                {
                    'q': 'Identify two sentences in your draft that make claims beyond what the data directly supports. Rewrite each sentence using appropriate hedging language.',
                    'answer_guide': 'Hedging examples: change "shows" to "suggests"; add "based on readings from a single station"; change "causes" to "is associated with"; add "further monitoring would be needed to confirm". Award marks for the quality of the original identification AND the rewrite.',
                    'marks': 6,
                },
            ],
            'vocabulary': [
                {'term': 'Data Journalism', 'definition': 'Journalism that uses quantitative data as primary source material, requiring skills in both statistical interpretation and writing.'},
                {'term': 'Cherry-Picking', 'definition': 'Selectively using data points that support a predetermined conclusion while ignoring contradictory evidence.'},
                {'term': 'Hedging Language', 'definition': 'Words and phrases that limit the certainty of a claim: "suggests", "may indicate", "consistent with", "appears to".'},
                {'term': 'Primary Source', 'definition': 'Original, uninterpreted data or firsthand accounts — as opposed to a secondary source that summarises or interprets primary data.'},
            ],
            'extension': (
                'Submit your article to your school newspaper or a local youth media outlet. '
                'Alternatively, send it to a real Nepali environmental organisation or NGO '
                'working in your district and ask for their feedback on both the data '
                'interpretation and the writing. Document their response.'
            ),
            'curriculum_link': 'Nepal CDC Grade 12 English, Unit 7: Journalistic Writing; Grade 11 Media Studies, Unit 4: Data and Reporting',
            'sdg_links': ['SDG 4: Quality Education', 'SDG 16: Peace, Justice and Strong Institutions', 'SDG 13: Climate Action'],
            'cross_curricular': [
                'Mathematics: Statistical interpretation, identifying misleading claims',
                'Social Studies: Right to information, government data, civic journalism',
                'Science: Evidence-based claims, uncertainty in data',
            ],
        },

        {
            'id': 'data-05',
            'title': 'Open Data, Open Science',
            'subtitle': 'Reproducibility, data ethics, and contributing to the scientific commons',
            'grade_band': 'UG',
            'subjects': ['Research Methods', 'Ethics', 'ICT', 'Philosophy of Science'],
            'duration': '90 min',
            'type': 'research',
            'overview': (
                'Undergraduate students examine the principles of open science and data ethics, '
                'evaluate the HICS dataset against FAIR principles, design a data governance '
                'framework for community-owned environmental data in Nepal, and contribute '
                'quality-controlled readings to the himalayansciences.org platform.'
            ),
            'nepal_context': (
                'Open data — freely accessible, machine-readable, openly licensed — is '
                'increasingly a requirement for scientific credibility and a condition of '
                'international research funding. But in Nepal, environmental data is often '
                'held in government ministries, donor-funded NGO databases, or foreign '
                'university research projects — not publicly accessible, not interoperable, '
                'and not cited. A community sensor network that openly shares its data '
                'contributes to global scientific knowledge while also asserting local '
                'ownership over local environmental information.'
            ),
            'learning_objectives': [
                'Articulate the FAIR data principles and evaluate a dataset against them.',
                'Identify ethical issues in environmental data collection, including consent, benefit-sharing and data sovereignty.',
                'Design a basic data governance framework appropriate for a community-owned sensor network in Nepal.',
                'Contribute quality-controlled data to an open repository with appropriate metadata.',
            ],
            'background': (
                'The open science movement argues that scientific knowledge — methods, data, '
                'software and publications — should be freely accessible to all, not locked '
                'behind journal paywalls or proprietary databases. The FAIR principles '
                '(Findable, Accessible, Interoperable, Reusable) are a practical framework '
                'for implementing open data. Findable means the data has a persistent '
                'identifier (like a DOI) and rich metadata. Accessible means it can be '
                'downloaded freely. Interoperable means it uses standard formats and '
                'vocabularies. Reusable means it has a clear license and sufficient '
                'documentation to be understood by others.\n\n'
                'Data ethics asks harder questions. Who consented to data being collected? '
                'Who benefits from the data — the community whose environment is monitored, '
                'or the researchers who publish it? Who has the right to delete data, '
                'correct errors, or restrict access? In the context of community-owned '
                'environmental monitoring, these questions are not theoretical. A sensor '
                'installed in a village without the community\'s knowledge and understanding '
                'violates principles of informed consent and local data sovereignty, even '
                'if the data itself is scientifically valuable.\n\n'
                'Data sovereignty is the principle that communities have the right to '
                'govern data about their own territories and environments. For Nepal\'s '
                'indigenous communities in particular, this matters: data about their land, '
                'resources and climate has historically been collected by outsiders for '
                'outsiders\' purposes. A genuinely community-owned sensor network changes '
                'this — but only if communities understand, control and benefit from the '
                'data it generates.'
            ),
            'teacher_notes': (
                'This activity sits at the intersection of science, ethics and policy. Push '
                'students beyond the technical FAIR principles to the harder questions of '
                'power and benefit. Who actually owns data collected by a sensor installed '
                'by an NGO in a community\'s field? Who should? What happens if the NGO\'s '
                'funding ends? These are real questions that Nepal\'s environmental data '
                'community has not yet fully resolved. Students who engage with them seriously '
                'are preparing for the frontier of their field.'
            ),
            'live_sensors': ['air_temp', 'air_hum', 'pressure', 'soil_temp', 'soil_moist'],
            'materials': ['Access to himalayansciences.org API documentation', 'Word processor'],
            'procedure': [
                'Access the HICS dashboard /api/data endpoint. Examine the JSON response. Evaluate it against each FAIR principle: is the data Findable, Accessible, Interoperable, Reusable? Score 1–4 for each.',
                'Identify THREE specific improvements to the API response or documentation that would increase the FAIR score.',
                'Case study: a foreign university installs 10 soil sensors across a farming village in Humla. They collect 2 years of data, publish a paper, and then the project ends. The sensors are removed and the data is kept on the university\'s server. Identify three ethical problems with this scenario.',
                'Design a data governance framework for a community-owned sensor network. Include: who controls access, how data is licensed, how the community benefits, what happens when the project ends.',
                'Export or record a set of quality-controlled readings with full metadata (station location, altitude, sensor model, calibration status). Write a 200-word data description following scientific repository standards.',
                'If API access is configured: submit one week of quality-controlled data to himalayansciences.org. Document the submission process.',
            ],
            'discussion_questions': [
                'Can environmental data be "owned"? If a community\'s rainfall is measured, who owns that measurement?',
                'Open data is presented as democratising knowledge — but who actually benefits most from freely available environmental data? Is this distribution equitable?',
                'Nepal\'s government holds climate and environmental data that could be used to validate community sensor readings. What would it take to make this data publicly accessible?',
            ],
            'worksheet_questions': [
                {
                    'q': 'Evaluate the HICS sensor API against each FAIR principle. Give a score out of 4 for each and justify your score with one specific observation.',
                    'answer_guide': 'F: likely 2–3 (data accessible at known URL but no persistent DOI, limited discovery metadata). A: 3–4 (freely accessible over local network). I: 2–3 (JSON is standard but no controlled vocabulary, no linked data). R: 2 (no explicit license, limited documentation). Award marks for quality of justification.',
                    'marks': 8,
                },
                {
                    'q': 'Define "data sovereignty" and explain why it is particularly relevant to indigenous communities and environmental monitoring in Nepal.',
                    'answer_guide': 'Data sovereignty: the right of a community to govern data collected about their territory or people. Relevant to Nepal because indigenous communities have historically had data about their land and resources collected by outsiders for outsiders\' benefit, without consent or benefit-sharing. Environmental sensor data about a community\'s field, water or air is information about their livelihood and territory.',
                    'marks': 5,
                },
            ],
            'vocabulary': [
                {'term': 'FAIR Principles', 'definition': 'A framework for scientific data management: data should be Findable, Accessible, Interoperable and Reusable.'},
                {'term': 'Data Sovereignty', 'definition': 'The right of communities or nations to govern and control data collected about their people, land and resources.'},
                {'term': 'Open License', 'definition': 'A legal mechanism (e.g. Creative Commons) that grants others the right to use, adapt and redistribute data or content.'},
                {'term': 'Persistent Identifier', 'definition': 'A long-term reference (such as a DOI) that identifies a digital resource and remains valid even if the resource moves.'},
            ],
            'extension': (
                'Draft a one-page "Community Data Agreement" for a fictional village in Nepal '
                'that agrees to host an IESH sensor station. The agreement should cover: '
                'who owns the data, who can access it, how the community benefits, what '
                'happens to the data and equipment if the project ends, and how disputes '
                'are resolved. Have it reviewed by a law or development studies lecturer '
                'if possible.'
            ),
            'curriculum_link': 'Undergraduate Research Methods / Information Science / Development Studies; aligns with Nepal\'s Right to Information Act 2007',
            'sdg_links': ['SDG 4: Quality Education', 'SDG 16: Strong Institutions', 'SDG 17: Partnerships', 'SDG 10: Reduced Inequalities'],
            'cross_curricular': [
                'Law / Policy: Data rights, intellectual property, consent frameworks',
                'Philosophy: Ethics of research, data ownership, power and knowledge',
                'ICT: APIs, data formats, repository standards',
                'Development Studies: Community participation, benefit-sharing',
            ],
        },
    ],
}
