ENVIRONMENT = {
    'id': 'environment',
    'title': 'Environment & Society',
    'icon': '🌏',
    'color': '#5eb85e',
    'tagline': 'Nepal\'s three worlds, one climate story — from the terai to the Himalaya',
    'description': (
        'Nepal is one of the world\'s most ecologically diverse countries — tropical plains, '
        'mid-hill forests, alpine meadows and permanent glaciers within 200 kilometres. '
        'It is also one of the most climate-vulnerable. This module connects sensor readings '
        'to the big picture: how ecosystems work, how communities depend on them, how '
        'traditional knowledge and modern science complement each other, and what it '
        'means to pursue justice in a world of unequal climate risk.'
    ),
    'sensors': ['air_temp', 'air_hum', 'pressure', 'soil_temp', 'soil_moist', 'mq7_raw', 'mq135_raw'],
    'teaching_guide': (
        'The environment module is the most explicitly values-oriented in the curriculum. '
        'While the science is real and rigorous, the activities deliberately connect data '
        'to equity, justice and tradition. Teachers should be comfortable with productive '
        'disagreement in the classroom — questions about who is responsible for climate change '
        'and what Nepal is owed do not have neat answers, and students who reach different '
        'conclusions from the same evidence are doing exactly the right thing. The traditional '
        'knowledge activity (env-03) requires sensitivity: local practices should be treated '
        'with genuine respect, not as curiosities to be compared against "real science". '
        'The goal is complementarity, not hierarchy.'
    ),
    'activities': [

        {
            'id': 'env-01',
            'title': 'Nepal\'s Three Worlds',
            'subtitle': 'How altitude shapes climate, ecology and human life',
            'grade_band': '6–8',
            'subjects': ['Geography', 'Science', 'Social Studies'],
            'duration': '35 min',
            'type': 'observation',
            'viz_type': 'altitude-zones',
            'viz_config': {
                'title': "Nepal's Three Ecological Zones — where does this station sit?",
                'zones': [
                    {
                        'name': 'Himalaya (Mountains)',
                        'min_m': 3000, 'max_m': 8848,
                        'color': '#a8c5da',
                        'emoji': '❄️',
                        'temp': '−15 to 10°C',
                        'desc': 'Glaciers, alpine meadows, yak herding, sparse population',
                    },
                    {
                        'name': 'Pahad (Mid-Hills)',
                        'min_m': 500, 'max_m': 3000,
                        'color': '#4a7c59',
                        'emoji': '🌿',
                        'temp': '15 to 25°C',
                        'desc': 'Terraced farming, forests, temperate crops, highest population',
                    },
                    {
                        'name': 'Terai (Plains)',
                        'min_m': 60, 'max_m': 500,
                        'color': '#2d6a4f',
                        'emoji': '🌾',
                        'temp': '25 to 40°C',
                        'desc': 'Hot and humid, rice paddies, sugarcane, major road networks',
                    },
                ],
                'fact': 'Nepal spans just 200 km north-to-south but contains nearly every climate zone on Earth.',
            },
            'overview': (
                'Students use the barometric pressure reading to estimate altitude, then '
                'explore how Nepal\'s three ecological zones (terai, hills, mountains) '
                'differ in climate, biodiversity and human activity — and how the sensor '
                'hub they are using would produce different readings in each zone.'
            ),
            'nepal_context': (
                'Nepal\'s extraordinary geographical compression — from 60 metres above sea '
                'level in the terai to 8,848 metres at the summit of Sagarmatha — means '
                'that the country contains almost every climate zone on Earth. A student in '
                'the hills experiences cooler temperatures and higher rainfall than a classmate '
                'in the terai. This is not just an interesting geography fact — it shapes what '
                'crops people grow, what diseases they face, how vulnerable their communities '
                'are to floods and droughts, and how climate change affects them.'
            ),
            'learning_objectives': [
                'Calculate approximate altitude from barometric pressure using the barometric formula.',
                'Describe the key differences in climate between Nepal\'s terai, hills and mountain zones.',
                'Explain why altitude causes temperature to decrease (environmental lapse rate).',
                'Predict what sensor readings would look like at a different altitude from the current station.',
            ],
            'background': (
                'Barometric pressure decreases predictably with altitude because there is less '
                'atmosphere above you as you ascend. At sea level, the full weight of the '
                'atmosphere presses down at about 1013 hPa. At 1,400 m (approximately '
                'Kathmandu\'s altitude), pressure is around 856 hPa. At Everest Base Camp '
                '(5,364 m), it is about 510 hPa. The barometric formula '
                'altitude = 44,330 × (1 − (P / 1013.25)^0.1903) gives a reasonable estimate '
                'from a pressure reading alone — the HICS dashboard calculates this for you.\n\n'
                'Temperature decreases with altitude at approximately 6.5°C per 1,000 metres '
                '— the environmental lapse rate. This is why the Himalaya have permanent snow '
                'while the terai at the same latitude is subtropical. The lapse rate also '
                'explains why Nepal\'s hill towns are pleasant in summer while Kathmandu '
                'valley can be hot, and why Nepal\'s mountain communities face extreme cold '
                'that terai communities never experience.\n\n'
                'Nepal\'s three ecological zones each have distinct biodiversity and land use. '
                'The terai\'s Sal forests and grasslands support Bengal tigers and one-horned '
                'rhinos. The mid-hills\' terraced agriculture — Nepal\'s most iconic landscape '
                '— produces rice, wheat, millet and vegetables. The high mountains, above the '
                'treeline, support yak herding and high-altitude crops like buckwheat and barley.'
            ),
            'teacher_notes': (
                'The altitude calculation on the dashboard makes Nepal\'s geography concrete '
                'and personal — the sensor is in the room with them, and its altitude is a '
                'real measurement of where they are. Use Google Earth or a printed elevation '
                'map of Nepal to show students where their station sits in the national '
                'landscape. Ask: "If we moved this sensor to Jiri, to Namche Bazaar, to '
                'the terai — what would change and what would stay the same?"'
            ),
            'live_sensors': ['pressure', 'air_temp', 'air_hum'],
            'materials': ['Nepal map (political + physical)', 'Calculator'],
            'procedure': [
                'Read the current pressure from the dashboard: ___ hPa. Use the formula altitude = 44,330 × (1 − (P ÷ 1013.25)^0.1903) to calculate the station\'s altitude. Compare with a map.',
                'Use the environmental lapse rate (6.5°C per 1,000 m) to estimate what the temperature would be 1,000 m higher. Then estimate 2,000 m higher. Show your working.',
                'Make a table: terai, hills, mountains. Fill in: typical altitude range, typical temperature range, typical annual rainfall, main crops/vegetation, key biodiversity.',
                'Predict: if this station were in Jumla (2,300 m) rather than your current location, what values would you expect for temperature, pressure and humidity? Explain your reasoning.',
                'Climate change question: which zone is warming fastest? (Answer: high mountains — do your own research and present a one-paragraph explanation.)',
            ],
            'discussion_questions': [
                'A family lives at 3,500 metres. How does altitude affect their daily life, work and health compared to a family at 500 metres?',
                'Nepal\'s glaciers are retreating. What happens to rivers and agriculture downstream as glaciers shrink?',
                'Why does Nepal have such high biodiversity in a relatively small area?',
            ],
            'worksheet_questions': [
                {
                    'q': 'The current pressure reading is P hPa. Use the barometric formula to calculate the altitude of this station in metres. Show every step of your calculation.',
                    'answer_guide': 'altitude = 44330 × (1 − (P/1013.25)^0.1903). Check that student has correctly used the current P value from the dashboard. Award full marks for correct working even if numerical answer differs slightly due to rounding. The key conceptual step is computing (P/1013.25)^0.1903 — check this is done correctly.',
                    'marks': 5,
                },
                {
                    'q': 'The environmental lapse rate is approximately 6.5°C per 1,000 m. If the current temperature at your station is T°C, estimate the temperature at the peak of a mountain 4,000 m higher. Show your working and discuss one reason why this estimate might be inaccurate.',
                    'answer_guide': 'Calculation: T − (6.5 × 4) = T − 26°C. Reasons for inaccuracy: actual lapse rate varies with humidity; above snow line, surface processes change; weather systems change temperature independently of altitude. Award marks for the quality of the inaccuracy discussion, not just the calculation.',
                    'marks': 4,
                },
            ],
            'vocabulary': [
                {'term': 'Environmental Lapse Rate', 'definition': 'The rate at which temperature decreases with altitude in the atmosphere — approximately 6.5°C per 1,000 metres.'},
                {'term': 'Barometric Formula', 'definition': 'A mathematical relationship between atmospheric pressure and altitude, derived from the physics of the atmosphere.'},
                {'term': 'Ecological Zone', 'definition': 'A geographic area with a characteristic climate, vegetation type and biodiversity, distinct from adjacent areas.'},
                {'term': 'Biodiversity', 'definition': 'The variety of living organisms in an area — including species diversity, genetic diversity and ecosystem diversity.'},
            ],
            'extension': (
                'Research Nepal\'s Koshi River system from its source in the Himalaya to its '
                'outflow into the Ganges. Draw a cross-section showing how altitude, temperature '
                'and rainfall change along its length. Annotate with the communities, agriculture '
                'and biodiversity associated with each zone.'
            ),
            'curriculum_link': 'Nepal CDC Grade 6–7 Social Studies: Geography of Nepal; Grade 7 Science: Atmosphere and Weather',
            'sdg_links': ['SDG 15: Life on Land', 'SDG 13: Climate Action', 'SDG 11: Sustainable Cities and Communities'],
            'cross_curricular': [
                'Mathematics: Barometric formula, percentage calculations',
                'Science: Atmosphere, lapse rate, ecosystems',
                'Social Studies: Nepal\'s regions, livelihoods, land use',
            ],
        },

        {
            'id': 'env-02',
            'title': 'How Environmental Systems Connect',
            'subtitle': 'Feedback loops, thresholds and why everything is connected to everything else',
            'grade_band': '9–10',
            'subjects': ['Environmental Science', 'Geography', 'Science'],
            'duration': '45 min',
            'type': 'analysis',
            'overview': (
                'Students observe simultaneous readings from multiple sensors and learn to '
                'think in systems — identifying feedback loops between variables like soil '
                'moisture, air humidity, temperature and plant health, and exploring what '
                'happens when these systems are disrupted.'
            ),
            'nepal_context': (
                'Nepal\'s ecosystems are deeply interconnected. Forests in the mid-hills '
                'regulate streams used for irrigation in the terai below. Glacier melt feeds '
                'rivers that supply water to millions of people. When deforestation removes '
                'trees from a hillside, it changes not only local biodiversity but also '
                'water retention, soil stability and downstream flood risk. Understanding '
                'these connections is essential for anyone working on Nepal\'s environmental '
                'management, disaster risk, or agricultural development.'
            ),
            'learning_objectives': [
                'Define positive and negative feedback loops with examples from the sensor data.',
                'Trace a causal chain connecting at least three environmental variables.',
                'Explain the concept of a tipping point and identify one real example relevant to Nepal.',
                'Evaluate the sensor hub as a monitoring tool for an interconnected system.',
            ],
            'background': (
                'Systems thinking is the practice of understanding how components of a system '
                'interact — not just what each component does independently. Environmental '
                'systems are characterised by feedback loops, where the output of a process '
                'affects its own input. A negative feedback loop stabilises a system: as '
                'temperature rises, evaporation increases, clouds form, sunlight is reflected, '
                'temperature falls. A positive feedback loop amplifies change: as Arctic ice '
                'melts, darker ocean water absorbs more heat, accelerating melting. Positive '
                'feedbacks drive climate tipping points.\n\n'
                'Between the sensor readings in this hub, several feedback relationships exist. '
                'Air humidity and soil moisture are connected — evaporation from soil increases '
                'air humidity. Air temperature affects evaporation rate, which affects humidity. '
                'In a real ecosystem, these would also connect to plant transpiration, cloud '
                'formation and rainfall. Monitoring multiple variables simultaneously lets '
                'us observe these relationships in real time.\n\n'
                'Tipping points occur when a system reaches a threshold beyond which change '
                'becomes self-reinforcing and difficult to reverse. Nepal\'s forest-rainfall '
                'system may have a tipping point: below a certain forest cover, rainfall '
                'decreases, making forest regrowth harder, further reducing rainfall. '
                'The Himalayan cryosphere — glaciers and permafrost — contains multiple '
                'tipping points that, once crossed, may be irreversible on human timescales.'
            ),
            'teacher_notes': (
                'The feedback loop concept is one of the most powerful ideas in science and '
                'one of the hardest for students to internalise intuitively. Spend time '
                'on concrete, local examples before moving to abstract definitions. Ask: '
                '"What happens to soil moisture when it gets hotter? What happens to plant '
                'health? What happens to air humidity? And then what happens to temperature?" '
                'Walking through this chain of consequences — and then asking what happens '
                'if you reverse the starting condition — builds the feedback loop intuition.'
            ),
            'live_sensors': ['air_temp', 'air_hum', 'soil_temp', 'soil_moist'],
            'materials': ['Graph paper for systems diagrams'],
            'procedure': [
                'Record simultaneous readings for all four sensors: air_temp, air_hum, soil_temp, soil_moist.',
                'Draw a systems diagram: place each variable in a circle and draw arrows showing causal connections. Label each arrow (+) for a positive relationship or (−) for a negative one.',
                'Trace the causal chain: what happens to air humidity if soil moisture increases? Trace through at least three variables.',
                'Identify a feedback loop in your diagram. Is it positive (amplifying) or negative (stabilising)? What real-world event might trigger this loop?',
                'Research: Nepal\'s Koshi Floods of 2008 (or another major environmental event). What role did feedback loops play in the disaster? Could it happen again?',
                'Present your systems diagram to the class. Explain which variable you believe is most critical to monitor — and why.',
            ],
            'discussion_questions': [
                'Why is monitoring only one environmental variable often not enough to understand what is happening in a place?',
                'If soil moisture drops very low during a dry season, describe the chain of effects this might have on air temperature and local rainfall over the following weeks.',
                'What would it take to restore a degraded hillside ecosystem? What feedback loops would you need to break or reverse?',
            ],
            'worksheet_questions': [
                {
                    'q': 'Draw and explain a feedback loop connecting air temperature and soil moisture. Identify whether it is a positive or negative feedback and explain why this matters for ecosystem stability.',
                    'answer_guide': 'Higher temperature → increased evaporation → lower soil moisture → less plant growth → less transpiration → lower air humidity (this is a chain, not a single loop). Or: higher temperature → higher evaporation → higher air humidity → potentially more rainfall → higher soil moisture (negative feedback stabilising the system). Award marks for the correct loop direction, the label, and the stability implications.',
                    'marks': 6,
                },
                {
                    'q': 'Explain what a tipping point is in an environmental system. Give ONE specific example from Nepal and describe what crossing the tipping point would mean for the communities that depend on that system.',
                    'answer_guide': 'Tipping point: a threshold beyond which change becomes self-reinforcing. Nepal examples: glacier retreat past a critical size (glacier-fed rivers become seasonal); deforestation past a threshold (rainfall reduction makes reforestation impossible); permafrost thaw (carbon release accelerates warming). Community impacts should be specific (water supply, flood risk, agricultural livelihoods).',
                    'marks': 5,
                },
            ],
            'vocabulary': [
                {'term': 'Feedback Loop', 'definition': 'A process where the output of a system influences its own input — either amplifying (positive) or dampening (negative) the original change.'},
                {'term': 'Tipping Point', 'definition': 'A threshold in a system beyond which change becomes self-reinforcing and may be difficult or impossible to reverse.'},
                {'term': 'Systems Thinking', 'definition': 'An approach to analysis that focuses on how a system\'s components interact, rather than examining each component in isolation.'},
                {'term': 'Cryosphere', 'definition': 'The frozen water part of the Earth\'s system: glaciers, ice sheets, permafrost and seasonal snow.'},
            ],
            'extension': (
                'Build a quantitative model. Use the historical data from the HICS dashboard '
                'to calculate the correlation between air temperature and air humidity over '
                'the last week. Does the correlation change at different times of day? '
                'What does this suggest about which feedback loop is dominant — '
                'evaporation-driven or solar-radiation-driven?'
            ),
            'curriculum_link': 'Nepal CDC Grade 9–10 Science: Environmental Science; Grade 10 Geography: Natural Ecosystems',
            'sdg_links': ['SDG 15: Life on Land', 'SDG 13: Climate Action', 'SDG 6: Clean Water'],
            'cross_curricular': [
                'Mathematics: Correlation, graphing causal chains',
                'Science: Evaporation, water cycle, ecosystems',
                'Social Studies: Land use, disaster risk, community vulnerability',
            ],
        },

        {
            'id': 'env-03',
            'title': 'Traditional Ecological Knowledge',
            'subtitle': 'What farmers and elders know that sensors can\'t measure — and what sensors add',
            'grade_band': '10–11',
            'subjects': ['Anthropology', 'Science', 'Social Studies', 'Agriculture'],
            'duration': '60 min',
            'type': 'observation',
            'overview': (
                'Students compare sensor readings with traditional ecological knowledge '
                'from the local community — weather prediction methods, soil assessment '
                'techniques, seasonal farming calendars — exploring how both knowledge '
                'systems are valuable and what they can learn from each other.'
            ),
            'nepal_context': (
                'Nepal\'s farming communities have accumulated thousands of years of '
                'ecological knowledge — understanding of rainfall patterns, soil types, '
                'pest cycles and seasonal variation that is passed down through generations. '
                'Much of this knowledge is not written down, is not recognised by formal '
                'institutions, and is at risk of being lost as younger generations '
                'migrate to cities. At the same time, climate change is making some '
                'traditional knowledge less reliable as familiar seasonal patterns shift. '
                'The relationship between traditional and scientific knowledge is not one '
                'of replacement but of complementarity — each has something to offer.'
            ),
            'learning_objectives': [
                'Document at least three examples of traditional ecological knowledge from a local elder or farmer.',
                'Compare a specific traditional weather or soil observation method with what the sensor measures.',
                'Evaluate when traditional knowledge is more reliable than sensor data, and vice versa.',
                'Discuss the ethics of documenting, sharing and using traditional knowledge.',
            ],
            'background': (
                'Traditional Ecological Knowledge (TEK) is the accumulated body of knowledge, '
                'practices and beliefs about the relationships between living organisms — '
                'including humans — and their environment, evolved by adaptive processes and '
                'handed down through generations. In Nepal, TEK includes: astronomical and '
                'weather forecasting traditions (reading clouds, wind direction, animal '
                'behaviour to predict rain); soil quality assessment by texture, colour and '
                'smell; crop variety selection based on altitude and microclimate; and '
                'water management practices embedded in community tole structures.\n\n'
                'TEK has real predictive value — generations of observation produce reliable '
                'pattern recognition. But TEK also has limitations: it encodes the climate '
                'conditions of the past, and as climate change shifts seasonal patterns, '
                'some traditional forecasting methods are becoming less reliable. Farmers '
                'in Nepal have reported that monsoon arrival patterns they relied on for '
                'decades are now increasingly unpredictable.\n\n'
                'Sensor data has complementary strengths and weaknesses. A temperature '
                'sensor measures precisely what it measures — but only at one point in space, '
                'only for as long as the battery holds, with no cultural context, no '
                'memory of last year\'s conditions, and no understanding of what the '
                'number means for farming. The combination of precise sensor data with '
                'rich traditional knowledge can produce understanding that neither '
                'achieves alone.'
            ),
            'teacher_notes': (
                'This activity requires preparation: ideally, invite a local farmer, '
                'elder or agricultural extension worker to the class before the session, '
                'or arrange for students to conduct interviews in the community. Treat '
                'traditional knowledge holders as genuine experts, not as historical '
                'curiosities. The ethics section is important: students should understand '
                'that documenting TEK without consent and benefit-sharing is a form of '
                'knowledge appropriation. There are real legal frameworks around this '
                '(the Nagoya Protocol on access and benefit-sharing).'
            ),
            'live_sensors': ['air_temp', 'air_hum', 'pressure', 'soil_moist', 'soil_temp'],
            'materials': ['Interview notes', 'Recording device (with permission)'],
            'procedure': [
                'Before class: interview a local farmer or elder. Ask: How do you know when the monsoon is coming? How do you assess whether soil is ready for planting? Have the seasons changed in your lifetime?',
                'In class: read the current sensor values. Describe what the sensor says about today\'s conditions.',
                'Compare: choose ONE traditional knowledge method. Describe how it works. Then describe what the sensor measures for the same phenomenon. What does each tell you that the other doesn\'t?',
                'Reliability test: over the next week, record both sensor readings and any traditional indicators observed (cloud type, wind direction, behaviour of specific plants or animals). Compare predictions.',
                'Ethics discussion: you have documented knowledge from a community member. Who owns this knowledge? What should you do before sharing it publicly?',
            ],
            'discussion_questions': [
                'In what situations would you trust a traditional weather prediction more than a barometric reading? In what situations less?',
                'Climate change is making some traditional seasonal forecasting less reliable. What does this mean for farming communities that depend on these predictions?',
                'Who benefits and who is at risk when traditional ecological knowledge is documented, published and shared widely?',
            ],
            'worksheet_questions': [
                {
                    'q': 'Document one traditional method for assessing soil quality or predicting weather that you learned in your community interviews. Describe: what the observation is, what it indicates, and how reliable it is believed to be.',
                    'answer_guide': 'Accept a wide range of genuine TEK observations. Award marks for: accurate description of the method, clarity about what it predicts, and any evidence of reliability assessment (either from the knowledge holder or from the student\'s own observation). Penalise if the student clearly did not conduct an interview.',
                    'marks': 5,
                },
                {
                    'q': 'Compare the traditional method you documented with what this sensor hub measures. What can the sensor tell you that the traditional method cannot? What can the traditional method tell you that the sensor cannot?',
                    'answer_guide': 'Sensors add: precision, continuous measurement, quantitative records, time series. TEK adds: cultural context, spatial knowledge of local microclimate, integration with farming practice, long historical baseline, no battery required, understanding of what numbers mean for agriculture. Award marks for the quality and depth of the comparison, not for preferring one over the other.',
                    'marks': 6,
                },
            ],
            'vocabulary': [
                {'term': 'Traditional Ecological Knowledge (TEK)', 'definition': 'Accumulated knowledge, practices and beliefs about the environment passed down through generations in a community.'},
                {'term': 'Bioindicator', 'definition': 'A living organism whose presence, absence or behaviour indicates something about environmental conditions — e.g. frogs indicating water quality.'},
                {'term': 'Nagoya Protocol', 'definition': 'An international agreement on access to genetic resources and traditional knowledge and the fair sharing of benefits from their use.'},
                {'term': 'Microclimate', 'definition': 'The climate of a small, specific area that differs from the general regional climate — often shaped by local topography, vegetation or water bodies.'},
            ],
            'extension': (
                'Design a "two-knowledge" monitoring system: a protocol that combines '
                'regular sensor readings with a structured diary of traditional ecological '
                'observations from a community member. What would you record? How often? '
                'How would you compare the two streams of information? Write the protocol '
                'as a one-page document suitable for giving to a participating farmer.'
            ),
            'curriculum_link': 'Nepal CDC Grade 11 Social Studies: Culture and Society; Agriculture: Traditional Farming; Science: Ecology',
            'sdg_links': ['SDG 2: Zero Hunger', 'SDG 15: Life on Land', 'SDG 11: Sustainable Communities'],
            'cross_curricular': [
                'Anthropology: Knowledge systems, oral tradition, community research',
                'Agriculture: Soil assessment, seasonal calendars, crop variety selection',
                'Ethics: Intellectual property, benefit-sharing, consent',
            ],
        },

        {
            'id': 'env-04',
            'title': 'Climate Justice and Nepal\'s Story',
            'subtitle': 'Who caused climate change, who suffers most, and what is owed',
            'grade_band': '11–12',
            'subjects': ['Ethics', 'Social Studies', 'Geography', 'English'],
            'duration': '60 min',
            'type': 'project',
            'overview': (
                'Students examine Nepal\'s position as a highly climate-vulnerable country '
                'with minimal historical responsibility for greenhouse gas emissions, '
                'and engage with the philosophical and political question of climate justice '
                '— using sensor data as a grounding point for abstract arguments.'
            ),
            'nepal_context': (
                'Nepal produces approximately 0.027% of global CO₂ emissions yet ranks among '
                'the world\'s 20 most climate-vulnerable countries. Its glaciers are retreating '
                'faster than almost anywhere else. Floods, droughts and landslides driven by '
                'erratic monsoon patterns are increasing. Communities that have maintained '
                'forest cover and kept their carbon footprints near zero are losing homes, '
                'crops and lives because of emissions produced on the other side of the world. '
                'This is the central injustice of climate change — and Nepal\'s case makes '
                'it visible with particular clarity.'
            ),
            'learning_objectives': [
                'Define climate justice and distinguish it from climate science.',
                'Describe Nepal\'s specific climate vulnerability and its causes.',
                'Evaluate at least two philosophical frameworks for assigning responsibility for climate harm.',
                'Construct a structured argument for or against a specific climate justice position.',
            ],
            'background': (
                'Climate justice is the argument that the harms of climate change are not '
                'distributed according to responsibility for causing it. Those who have '
                'emitted the most greenhouse gases — historically, wealthy industrialised '
                'nations — have the greatest capacity to adapt to climate change. Those who '
                'have emitted the least — small island nations, landlocked mountain countries, '
                'sub-Saharan Africa — often face the greatest harm and have the least '
                'resources to adapt. This distribution is not random; it tracks the same '
                'inequalities of economic power that structured colonialism.\n\n'
                'Nepal\'s climate vulnerability has several specific dimensions. The '
                'Himalayas are warming at twice the global average rate. Glacial Lake '
                'Outburst Floods (GLOFs) — triggered by rapid glacial retreat — destroy '
                'downstream villages with little warning. Monsoon rainfall has become more '
                'variable and intense, increasing both flood and drought risk. High-altitude '
                'communities dependent on consistent snowfall for water storage are facing '
                'water insecurity in a country that was once considered water-rich.\n\n'
                'Philosophical frameworks for thinking about responsibility include: '
                'polluter pays (those who emitted should compensate those who suffer — '
                'but many historical emitters are now dead); capacity to pay (wealthy '
                'nations should pay because they can, regardless of historical responsibility); '
                'common but differentiated responsibility (the principle enshrined in the '
                'UNFCCC — all nations share responsibility but in proportion to their '
                'capabilities and historical emissions). None of these frameworks resolves '
                'all disputes; the disagreements between them are the central political '
                'tensions of international climate negotiations.'
            ),
            'teacher_notes': (
                'The question "what is Nepal owed?" does not have a single correct answer, '
                'and this activity is not designed to produce one. What it is designed to '
                'produce is students who can make rigorous, evidence-based arguments on '
                'multiple sides of the question. The CO₂ sensor data grounds the '
                'discussion: the MQ-135 readings in this room are real measurements of '
                'CO₂ and VOC levels. Ask students: "What produced the CO₂ in this room? '
                'What produces it globally? Who decides how much is acceptable?"'
            ),
            'live_sensors': ['air_temp', 'mq7_raw', 'mq135_raw'],
            'materials': ['Writing materials'],
            'procedure': [
                'Read the current MQ-135 reading and reflect: this sensor detects CO₂ and VOCs in this room. What global processes produce CO₂ at a scale that is changing the climate?',
                'Research: Nepal\'s share of global CO₂ emissions (approximately 0.027%). Its Human Development Index ranking. Its climate vulnerability ranking. What is the relationship between these three numbers?',
                'Philosophical frameworks: read descriptions of "polluter pays", "capacity to pay" and "common but differentiated responsibility". Which framework do you find most compelling? Why?',
                'Stakeholder positions: research the stated positions of Nepal\'s government, a wealthy G20 nation, and a small island state in UNFCCC negotiations. What are the key differences?',
                'Write a 500-word essay: "What is Nepal owed for climate harm it did not cause?" Structure your essay as a genuine argument — claim, evidence, counterargument, response.',
            ],
            'discussion_questions': [
                'A family in Humla loses their home to a GLOF caused by glacial retreat. Who is responsible for this harm, and who should pay for their losses?',
                'Nepal\'s new airport, dams, and infrastructure will increase its CO₂ emissions. Does development forfeit Nepal\'s moral claim to climate compensation?',
                'What is "loss and damage" in climate negotiations, and why do wealthy nations resist committing to it?',
            ],
            'worksheet_questions': [
                {
                    'q': 'Nepal emits approximately 0.027% of global CO₂ but is one of the world\'s 20 most climate-vulnerable countries. Use ONE specific philosophical framework (polluter pays, capacity to pay, or common but differentiated responsibility) to argue what Nepal is owed. Be specific about what should be provided, by whom, and on what timeline.',
                    'answer_guide': 'Award marks for: correct identification and explanation of the chosen framework; specific claims about what Nepal should receive (adaptation finance, loss and damage payments, technology transfer); identification of who the responsible parties are; a realistic timeline or mechanism. Penalise vague generalisations. Do not penalise students for the position they take — award marks for the quality of the argument.',
                    'marks': 8,
                },
                {
                    'q': 'Write a one-paragraph counterargument to the position you took above. What is the strongest case against your position?',
                    'answer_guide': 'Counterarguments might include: difficulty of attributing specific harms to specific emitters; problems with historical liability when historical emitters are dead; "luxury emissions vs. survival emissions" distinction (poor countries\' new emissions are harder to restrict); practical problems with international enforcement of climate obligations. Award marks for engaging genuinely with the counterargument, not for weakening it.',
                    'marks': 4,
                },
            ],
            'vocabulary': [
                {'term': 'Climate Justice', 'definition': 'The principle that the burdens and benefits of climate change and climate action should be distributed equitably across nations and peoples.'},
                {'term': 'Loss and Damage', 'definition': 'In climate negotiations, the category of climate harms that go beyond what adaptation can prevent — permanent losses that require compensation.'},
                {'term': 'GLOF (Glacial Lake Outburst Flood)', 'definition': 'A sudden release of water stored in a glacial lake, caused by failure of a natural ice or moraine dam — a major disaster risk in Nepal.'},
                {'term': 'Common but Differentiated Responsibility', 'definition': 'The UNFCCC principle that all nations share responsibility for climate change, but in proportion to their historical emissions and current capabilities.'},
            ],
            'extension': (
                'Write a letter from the perspective of a Nepali farmer in Humla to the '
                'government of a major historical CO₂ emitter (UK, USA, Germany — your '
                'choice). The letter should explain specifically how climate change has '
                'affected the farmer\'s life and make a concrete, specific request for '
                'redress. Research the Humla district to make the letter geographically '
                'and culturally accurate.'
            ),
            'curriculum_link': 'Nepal CDC Grade 12 Social Studies: Global Issues; Grade 11 English: Argumentative Writing; Grade 11 Optional Ethics',
            'sdg_links': ['SDG 13: Climate Action', 'SDG 10: Reduced Inequalities', 'SDG 16: Justice and Strong Institutions'],
            'cross_curricular': [
                'Ethics and Philosophy: Justice frameworks, moral responsibility',
                'Geography: Climate vulnerability, Nepal\'s Himalayan geography',
                'Mathematics: Percentages, proportional reasoning about emissions',
                'English: Argumentative writing, essay structure',
            ],
        },

        {
            'id': 'env-05',
            'title': 'From Data to Policy',
            'subtitle': 'How environmental monitoring shapes law, governance and development planning',
            'grade_band': 'UG',
            'subjects': ['Development Studies', 'Policy', 'Environmental Science', 'Law'],
            'duration': '90 min',
            'type': 'research',
            'overview': (
                'Undergraduate students trace the pathway from raw sensor data to policy '
                'action — examining how environmental monitoring informs Nepal\'s legal '
                'frameworks, development planning processes, and community-level governance. '
                'They then design a monitoring-to-policy brief for a real issue in their '
                'community or district.'
            ),
            'nepal_context': (
                'Nepal\'s Constitution of 2015 recognises the right to a clean environment '
                'as a fundamental right (Article 30). The Environment Protection Act (2019) '
                'requires environmental impact assessment for major projects. Nepal\'s NDC '
                '(Nationally Determined Contribution) under the Paris Agreement commits to '
                'specific emissions reductions and adaptation measures. But between these '
                'legal commitments and the reality on the ground lies an enormous '
                'implementation gap — often because the monitoring data needed to enforce '
                'the law and evaluate outcomes simply does not exist at the local level. '
                'Community sensor networks like IESH can begin to close this gap.'
            ),
            'learning_objectives': [
                'Trace the pathway from raw environmental data to policy decision with specific real examples.',
                'Evaluate Nepal\'s legal framework for environmental protection against international standards.',
                'Identify at least three specific ways that community sensor data could inform local or national policy in Nepal.',
                'Produce a policy brief that uses sensor data as evidence for a specific recommendation.',
            ],
            'background': (
                'The science-policy interface is the space where scientific evidence meets '
                'political decision-making. In environmental governance, this interface is '
                'mediated by institutions — the IPCC produces assessments that inform the '
                'UNFCCC negotiations; national monitoring agencies produce data that informs '
                'environmental protection regulations; local sensor networks produce evidence '
                'for municipal planning. At each level, the quality, availability and '
                'credibility of data determines the quality of policy.\n\n'
                'Nepal\'s environmental governance has improved significantly in recent '
                'decades. The 2019 Environment Protection Act significantly strengthens '
                'environmental impact assessment requirements and establishes pollution '
                'standards for air, water and soil. The National Adaptation Plan (2021) '
                'sets out a comprehensive framework for adapting to climate change. But '
                'enforcement depends on monitoring — and Nepal\'s official monitoring '
                'network remains thin, particularly outside Kathmandu. The Kathmandu '
                'valley\'s chronic air pollution problem, for example, has been well '
                'documented by monitoring stations for years; regulatory action has been '
                'much slower to follow.\n\n'
                'Community-level data has a specific role in this system. It can provide '
                'evidence at spatial scales that national networks cannot cover. It can '
                'be used to hold local authorities accountable to national standards. '
                'It can document harm — needed for legal action or compensation claims. '
                'And it can be used by community members themselves to make evidence-based '
                'arguments in local governance processes, from school health standards '
                'to agricultural support requests to disaster risk planning.'
            ),
            'teacher_notes': (
                'The policy brief is a genuine professional document — encourage students '
                'to think of their audience as a real policymaker (ward chairperson, '
                'district environment officer, municipal planner) and to write accordingly. '
                'The best policy briefs are concrete and actionable: not "improve air '
                'quality" but "install one additional air quality monitoring station at '
                'the school junction and enforce the no-idling zone under EPA section 27". '
                'Encourage students to identify a real policymaker in their area and '
                'consider actually sending the brief.'
            ),
            'live_sensors': ['air_temp', 'air_hum', 'pressure', 'soil_temp', 'soil_moist', 'mq7_raw', 'mq135_raw'],
            'materials': ['Nepal EPA 2019', 'Nepal NDC text', 'Policy brief template'],
            'procedure': [
                'Map the pathway: choose one real Nepal environmental policy (e.g. EPA 2019 air quality standards, or the NDC renewable energy target). Trace the evidence chain: what data was used to set the standard? Who collected it? Who evaluated it? Who decided?',
                'Identify the gap: where in the pathway from sensor to policy is the data chain weakest? What data is missing that would make the policy more effective?',
                'Evaluate the HICS station: what policy-relevant information does this device collect? Which of Nepal\'s environmental standards is relevant to its readings?',
                'Design a use case: describe a specific scenario where a community sensor network like IESH could be used as evidence in a local governance process. Be specific about: who presents the data, to whom, in what forum, for what decision.',
                'Write a policy brief (600–800 words) recommending one specific policy action that the sensor data supports. Structure: Context (100 words), Evidence (200 words), Recommendation (200 words), Implementation (200 words), Risks (100 words).',
            ],
            'discussion_questions': [
                'A community uses IESH sensor data to document that air quality near a brick kiln violates EPA standards. What legal options do they have? What practical obstacles might they face?',
                'Nepal\'s government uses data from foreign satellites and international research institutions to set environmental policy. What are the advantages and risks of this dependency?',
                'Who should decide what level of air pollution is "acceptable" in a community — the community itself, national regulators, or international scientific bodies? On what basis?',
            ],
            'worksheet_questions': [
                {
                    'q': 'Identify ONE specific monitoring gap in Nepal\'s current environmental governance (at local, district or national level). Describe: what data is missing, why it matters, and how a community sensor network like IESH could begin to fill it.',
                    'answer_guide': 'Examples: no local air quality monitoring outside Kathmandu; no school-level indoor air quality data; no community-level soil health monitoring for agricultural planning; no river quality monitoring in rural areas. Award marks for the specificity of the gap identification, the reasoning about why it matters (what decisions are being made without this data), and the realism of the proposed sensor solution.',
                    'marks': 7,
                },
                {
                    'q': 'What is the science-policy interface? Describe ONE mechanism through which community sensor data could enter the formal policy process in Nepal, identifying the specific institution or process it would feed into.',
                    'answer_guide': 'Science-policy interface: the processes and institutions through which scientific evidence informs policy decisions. Mechanisms: EIA (Environmental Impact Assessment) public comments; ward and municipality development plans; district disaster risk management plans; public environmental monitoring registers under EPA 2019; formal complaints to Department of Environment. Award marks for identifying a real, specific mechanism (not just "give data to the government").',
                    'marks': 5,
                },
            ],
            'vocabulary': [
                {'term': 'NDC (Nationally Determined Contribution)', 'definition': 'A country\'s climate action plan submitted to the UNFCCC under the Paris Agreement, specifying emissions reductions and adaptation commitments.'},
                {'term': 'Environmental Impact Assessment (EIA)', 'definition': 'A formal process for evaluating the likely environmental effects of a proposed development project before permission is granted.'},
                {'term': 'Science-Policy Interface', 'definition': 'The processes, institutions and actors that mediate between scientific knowledge production and policy decision-making.'},
                {'term': 'Monitoring Gap', 'definition': 'A geographic area, time period, or variable for which systematic environmental data is absent, creating blind spots in governance.'},
            ],
            'extension': (
                'Submit your policy brief to a real recipient — your ward chairperson, your '
                'school\'s municipal education officer, or your district environment office. '
                'Document the submission and any response. What happened? What would '
                'need to change for community sensor data to be taken seriously by local '
                'governance institutions in Nepal? Write a one-page reflection.'
            ),
            'curriculum_link': 'Undergraduate Environmental Science, Development Studies, Law; Nepal EPA 2019; Nepal NDC 2020',
            'sdg_links': ['SDG 16: Strong Institutions', 'SDG 13: Climate Action', 'SDG 15: Life on Land', 'SDG 17: Partnerships'],
            'cross_curricular': [
                'Law: Environmental law, fundamental rights, EPA 2019',
                'Development Studies: Science-policy interface, governance, community participation',
                'Science: Evidence standards, monitoring methodology',
                'English: Policy writing, audience-specific communication',
            ],
        },

        {
            'id': 'env-sky',
            'title': 'Night Sky & Meteor Detection',
            'subtitle': 'Sky brightness, light pollution, and detecting meteors with a camera',
            'grade_band': '9–11',
            'subjects': ['Physics', 'Environmental Science', 'Astronomy'],
            'duration': '60 min (plus optional night observation)',
            'type': 'observation',
            'viz_type': 'sky-cam',
            'viz_config': {'title': 'Live sky — observe and record what you see'},
            'overview': (
                'Nepal sits at the edge of some of the world\'s last truly dark skies — high-altitude '
                'sites in the Himalaya see the Milky Way with the naked eye. Yet even here, light '
                'pollution is creeping in. In this activity students use the station\'s sky camera '
                'and brightness sensor to quantify sky darkness, observe or reconstruct meteor events, '
                'and connect sky quality to both scientific access and cultural heritage.'
            ),
            'nepal_context': (
                'The International Dark-Sky Association recognises that altitude and isolation give '
                'Nepal\'s mountains some of the lowest artificial sky glow in Asia. Yet rapid '
                'development of hill towns and trekking lodges is changing this fast. Nagarkot, '
                'just 32 km from Kathmandu, was once famous for clear Himalayan night skies; '
                'today light from the valley significantly brightens the eastern horizon. '
                'The Perseids (August), Leonids (November) and Geminids (December) are all visible '
                'from Nepal with peak rates of 50–150 meteors/hour under dark skies.'
            ),
            'teacher_notes': (
                'This activity has two parts: a classroom/daytime component (sky brightness analysis, '
                'light pollution concepts) and an optional night-time observation. The night component '
                'requires permission and safety planning but is very high-impact. If night observation '
                'is not possible, use archived images from the station camera. The meteor detection '
                'methodology (frame differencing) is a gateway into computer vision — a natural '
                'extension for CS/IT interested students.'
            ),
            'live_sensors': ['air_temp', 'pressure', 'altitude'],
            'materials': ['Sky camera (this station)', 'Graph paper or spreadsheet', 'Dark red torch for night use'],
            'procedure': [
                'Measure sky brightness: observe the brightness value shown by the station (0–255 scale). Record it now, then compare to a night reading if available in the image history.',
                'Light pollution mapping: look at the live image. Which directions show the brightest horizon glow? What human settlements or infrastructure lie in those directions?',
                'Estimate cloud cover: use the station\'s cloud cover % and compare to your own visual estimate. How would cloud cover affect a night sky observation?',
                'Meteor detection method: explain in your own words how frame-differencing works — comparing two consecutive images and highlighting pixels that changed. Why would this flag meteors?',
                'Classify a streak: if any linear streak appears in the sky image, estimate its angular length, direction, and whether it could be a meteor, aircraft, or satellite. Give reasons.',
                'Bortle scale: use the station\'s night brightness reading to estimate the Bortle class of this site (1=darkest, 9=city). What would need to change to improve it by one class?',
            ],
            'discussion_questions': [
                'The sky camera brightness reads 8 at midnight. What does this tell you about cloud cover vs. light pollution? What extra measurements would help distinguish the two causes?',
                'Meteor detection requires capturing fast streaks on slow hardware. The OV5647 runs at ~15 fps at full resolution. What frame rate and exposure would you need to reliably capture a meteor moving at 70 km/s across 10° of sky?',
                'Light pollution is rarely discussed as an environmental problem in Nepal. Who does it harm? Who benefits from the lights that cause it? Is it worth regulating?',
            ],
            'worksheet_questions': [
                {
                    'q': 'A meteor enters the atmosphere at 40 km/s and produces a visible streak for 0.3 seconds. Calculate the length of the streak in km, assuming it travels at an altitude of 100 km.',
                    'answer_guide': 'Distance = speed × time = 40,000 m/s × 0.3 s = 12,000 m = 12 km. Accept 10–15 km range with working shown.',
                    'marks': 3,
                },
                {
                    'q': 'Explain the frame-differencing technique for meteor detection. Why would aircraft and satellites also be flagged, and how could you distinguish them from meteors?',
                    'answer_guide': 'Frame differencing: subtract consecutive frames; changed pixels mark a moving object. Aircraft: dashed/intermittent streak (flashing nav lights ~1 Hz); satellite: slow consistent arc, visible only in twilight; meteor: continuous bright streak, duration <1 s, no colour change. Award marks for explaining differencing and identifying specific distinguishing features.',
                    'marks': 5,
                },
            ],
            'vocabulary': [
                {'term': 'Bortle Scale', 'definition': 'A nine-level scale measuring night sky darkness. Class 1 is the darkest; class 9 is the most light-polluted inner-city sky.'},
                {'term': 'Frame Differencing', 'definition': 'A computer vision technique detecting motion by comparing two consecutive frames and highlighting pixels that changed.'},
                {'term': 'Meteor Shower Radiant', 'definition': 'The point in the sky from which a shower\'s meteors appear to originate — caused by Earth entering a stream of cometary debris.'},
                {'term': 'Sky Brightness', 'definition': 'How bright the night sky appears, combining natural sources (stars, airglow) and artificial light pollution.'},
                {'term': 'Light Pollution', 'definition': 'Excessive artificial light brightening the night sky, wasting energy and harming astronomy, ecosystems, and human sleep.'},
            ],
            'extension': (
                'Write a Python script that loads two consecutive camera images and computes the '
                'absolute difference image using Pillow. Apply a threshold to suppress noise and '
                'count "bright streak" pixels. Test it on any two images from the station archive.'
            ),
            'curriculum_link': 'Grade 9–11 Physics (Nepal CDC): Light, Optics; Grade 11 Environmental Science: Pollution; Grade 10 ICT',
            'sdg_links': ['SDG 11: Sustainable Cities', 'SDG 4: Quality Education', 'SDG 15: Life on Land'],
            'cross_curricular': [
                'Physics: Wave optics, electromagnetic spectrum, kinematics',
                'Computer Science: Image processing, frame differencing, pixel arrays',
                'Environmental Science: Light pollution, urban development impacts',
                'Mathematics: Speed-distance-time, angular measurement',
            ],
        },
    ],
}
