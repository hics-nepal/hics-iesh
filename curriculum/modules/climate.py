CLIMATE = {
    'id': 'climate',
    'title': 'Climate & Atmosphere',
    'icon': '🌤',
    'color': '#58a6ff',
    'tagline': 'Reading the air above us — temperature, humidity, pressure and altitude',
    'description': (
        'The atmosphere is the thin envelope of air that makes life possible on Earth. '
        'This module uses live temperature, humidity and barometric pressure readings to '
        'explore how the atmosphere works, how Nepal\'s remarkable geography shapes its '
        'climate, and how long-term changes in these measurements connect to the global '
        'climate crisis.'
    ),
    'sensors': ['air_temp', 'air_hum', 'pressure', 'altitude'],
    'teaching_guide': (
        'This module works best when students have access to the live dashboard during the '
        'activity. Encourage students to record readings at the start and end of each session '
        'and to notice changes. For grade 6–9 activities, focus on observation and description '
        'before explanation. For grade 11–UG activities, push students toward quantitative '
        'analysis and to question the limits of a single measurement station. The Nepal context '
        'sections are central — avoid treating climate as an abstract global topic when it has '
        'immediate, visible consequences in every Nepali valley and hillside.'
    ),
    'activities': [

        {
            'id': 'climate-01',
            'title': 'What the Air Around Us Tells Us',
            'subtitle': 'Reading three invisible measurements that describe your environment',
            'grade_band': '6–8',
            'subjects': ['Science', 'Geography'],
            'duration': '30 min',
            'type': 'observation',
            'viz_type': 'hz-gauges',
            'viz_config': {
                'title': 'What is the air like right now at this station?',
                'gauges': [
                    {
                        'key': 'air_temp', 'label': 'Air Temperature', 'unit': '°C',
                        'min': 0, 'max': 40,
                        'zones': [
                            {'label': 'Cool', 'color': '#4a9eff', 'pct': 30},
                            {'label': 'Comfortable', 'color': '#3fb950', 'pct': 35},
                            {'label': 'Warm', 'color': '#d29922', 'pct': 20},
                            {'label': 'Hot', 'color': '#f85149', 'pct': 15},
                        ],
                        'fact': 'Temperature drops about 6°C for every 1,000 m you climb.',
                    },
                    {
                        'key': 'air_hum', 'label': 'Humidity', 'unit': '%',
                        'min': 0, 'max': 100,
                        'zones': [
                            {'label': 'Dry', 'color': '#d29922', 'pct': 20},
                            {'label': 'Comfortable', 'color': '#3fb950', 'pct': 30},
                            {'label': 'Humid', 'color': '#58a6ff', 'pct': 30},
                            {'label': 'Saturated', 'color': '#8b949e', 'pct': 20},
                        ],
                        'fact': 'Nepal\'s monsoon pushes humidity above 80% for months.',
                    },
                    {
                        'key': 'pressure', 'label': 'Pressure', 'unit': 'hPa',
                        'min': 850, 'max': 1013,
                        'zones': [
                            {'label': 'High alt.', 'color': '#bc8cff', 'pct': 40},
                            {'label': 'Mid alt.', 'color': '#58a6ff', 'pct': 35},
                            {'label': 'Low alt.', 'color': '#3fb950', 'pct': 25},
                        ],
                        'fact': 'Sea-level pressure is ~1013 hPa. Lower reading = higher altitude.',
                    },
                ],
            },
            'overview': (
                'Students take their first readings from the sensor hub, learn what temperature, '
                'humidity and pressure actually measure, and connect those numbers to what they '
                'can feel and observe outside.'
            ),
            'nepal_context': (
                'Nepal spans five climate zones within a horizontal distance of just 200 km — '
                'from the hot, humid Terai lowlands at 60 m above sea level to the frozen '
                'Himalayan peaks above 8,000 m. The air on a summer morning in Janakpur feels '
                'completely different from air in Namche Bazaar, and the sensor numbers reflect '
                'that difference precisely. Nepali farmers have read weather signals for centuries '
                'through cloud patterns, wind direction and the behaviour of animals. This lesson '
                'adds numerical precision to that traditional literacy.'
            ),
            'learning_objectives': [
                'Explain what temperature, humidity and atmospheric pressure measure in physical terms.',
                'Read live sensor values and record them accurately in a data table.',
                'Describe how the three measurements relate to what we feel as "weather".',
                'Connect Nepal\'s geographical diversity to differences in climate across the country.',
            ],
            'background': (
                'Temperature measures how much kinetic energy the air molecules have — faster-moving '
                'molecules feel hot, slower ones feel cold. We measure it in degrees Celsius (°C). '
                'Air temperature changes through the day as the sun heats surfaces and the ground '
                'radiates that heat back into the air. It also changes with altitude: for every '
                '1,000 m you climb, the air is roughly 6°C cooler.\n\n'
                'Humidity tells us how much water vapour is in the air as a percentage of the maximum '
                'it could hold at that temperature. At 100% humidity, the air is saturated — water '
                'starts to condense as dew, fog or rain. Nepal\'s monsoon brings humidity levels above '
                '80% for months at a time. High humidity makes hot temperatures feel even hotter '
                'because sweat cannot evaporate efficiently to cool the body.\n\n'
                'Atmospheric pressure is the weight of the entire column of air above you pressing '
                'down. At sea level this is approximately 1,013 hPa (hectopascals). As you go higher, '
                'there is less air above you and pressure falls. This is why our sensor can estimate '
                'altitude from the pressure reading alone — the relationship between the two is '
                'described by the barometric formula, which we will explore in a later activity.'
            ),
            'teacher_notes': (
                'Students often confuse temperature with heat — emphasise that temperature is a '
                'property of the air itself, while heat is energy being transferred. If the class '
                'is outdoors or near a window, ask students to note whether the sensor reading '
                'matches what their body tells them. Discrepancies (the sensor is in the shade, '
                'the room is air-conditioned) are valuable teaching moments about measurement context.'
            ),
            'live_sensors': ['air_temp', 'air_hum', 'pressure'],
            'materials': ['Notebook', 'Pencil', 'Printed data table worksheet (optional)'],
            'procedure': [
                'Open the HICS dashboard on your device and navigate to the Climate section.',
                'Record today\'s air temperature, humidity and pressure in your notebook.',
                'Step outside (or look out the window). Write three observations about the weather using only your senses — what you see, feel, hear.',
                'Return to the sensor readings. Can you match each observation to one of the three numbers?',
                'Record the sensor values again 15 minutes later. Have any changed? By how much?',
                'Sketch a simple table with columns: Location (Terai / Hills / Mountains), Expected Temperature, Expected Humidity, Expected Pressure. Fill in what you think the values might be for each region today.',
            ],
            'discussion_questions': [
                'If the temperature outside is 28°C and the humidity is 85%, how would you expect to feel? What about 28°C at 30% humidity?',
                'Why might farmers in Nepal care deeply about humidity levels in April and May?',
                'The pressure reading at our station is lower than 1,013 hPa. What does that tell us about where our station is located?',
            ],
            'worksheet_questions': [
                {
                    'q': 'Record the three sensor readings right now. Temperature: ___ °C   Humidity: ___ %   Pressure: ___ hPa',
                    'answer_guide': 'Observational — accept any accurate reading. Check students are reading the correct units.',
                    'marks': 3,
                },
                {
                    'q': 'In your own words, explain what humidity means. Use an example from daily life in Nepal.',
                    'answer_guide': 'Should include the idea of water vapour in the air. Good examples: damp clothes taking longer to dry in monsoon, sweat not evaporating on a humid day, morning dew on fields.',
                    'marks': 3,
                },
                {
                    'q': 'If you travelled from Kathmandu (1,400 m) to a village at 3,000 m, would the pressure reading increase or decrease? Explain why.',
                    'answer_guide': 'Decrease — there is less air above you at higher altitude, so the weight of the air column pressing down is less.',
                    'marks': 2,
                },
                {
                    'q': 'List TWO ways that high humidity affects daily life in Nepal during the monsoon.',
                    'answer_guide': 'Accept any two reasonable answers: clothes stay damp, mould grows faster, heat feels more intense, crops receive adequate moisture, rivers flood, landslide risk increases.',
                    'marks': 2,
                },
            ],
            'vocabulary': [
                {'term': 'Temperature', 'definition': 'A measure of the average kinetic energy of air molecules, expressed in degrees Celsius (°C).'},
                {'term': 'Relative Humidity', 'definition': 'The amount of water vapour in the air expressed as a percentage of the maximum possible at that temperature.'},
                {'term': 'Atmospheric Pressure', 'definition': 'The force exerted by the weight of the air column above a point, measured in hectopascals (hPa).'},
                {'term': 'Climate Zone', 'definition': 'A region with a broadly consistent pattern of temperature, rainfall and seasonal change.'},
            ],
            'extension': (
                'Research Nepal\'s five development regions and find the average annual temperature '
                'and rainfall for one location in each. Create a comparison table and write a '
                'paragraph explaining how altitude drives these differences.'
            ),
            'curriculum_link': 'Nepal CDC Grade 7 Compulsory Science, Unit 3: Weather and Climate; Grade 7 Social Studies, Unit 2: Physical Features of Nepal',
            'sdg_links': ['SDG 13: Climate Action', 'SDG 4: Quality Education'],
            'cross_curricular': [
                'Mathematics: Recording data in tables, reading decimal numbers',
                'Nepali: Describing weather — weather vocabulary in Nepali',
                'Social Studies: Nepal\'s geographical regions and altitude zones',
            ],
        },

        {
            'id': 'climate-02',
            'title': 'The Monsoon in Numbers',
            'subtitle': 'How Nepal\'s defining weather pattern shows up in sensor data',
            'grade_band': '8–10',
            'subjects': ['Science', 'Mathematics', 'Social Studies'],
            'duration': '45 min',
            'type': 'analysis',
            'overview': (
                'Students analyse temperature and humidity data from the dashboard, identify '
                'the signature of Nepal\'s monsoon season, and explore how this single weather '
                'pattern shapes agriculture, festivals, disasters and daily life.'
            ),
            'nepal_context': (
                'Nepal receives approximately 80% of its annual rainfall between June and '
                'September — the summer monsoon driven by the temperature difference between '
                'the Indian subcontinent and the Bay of Bengal. Without the monsoon, Nepal\'s '
                'terraced rice paddies, which feed the majority of the population, cannot '
                'function. But the monsoon also brings floods, landslides and disease. '
                'Climate change is shifting monsoon onset dates and increasing the intensity '
                'of extreme rainfall events, threatening a system that Nepali civilisation '
                'has been built around for millennia.'
            ),
            'learning_objectives': [
                'Read a time-series graph and identify trends, peaks and troughs.',
                'Calculate the mean temperature and mean humidity from a data set.',
                'Explain the mechanism driving Nepal\'s monsoon using temperature and pressure concepts.',
                'Evaluate the social and economic consequences of monsoon variability for Nepal.',
            ],
            'background': (
                'The monsoon is not simply a rain season — it is a large-scale reversal of wind '
                'direction driven by differential heating. In summer, the land mass of South Asia '
                'heats up far more quickly than the Indian Ocean. Hot land creates low pressure '
                'over the continent; the relatively cooler ocean maintains higher pressure. Air '
                'flows from high pressure to low, bringing moisture-laden ocean air northward '
                'and inland. As this air rises over the Himalayas and cools, it releases its '
                'moisture as rain — sometimes over 200 mm in a single day in the hills.\n\n'
                'On a sensor, the monsoon arrival shows up clearly: humidity rises sharply from '
                'below 50% to consistently above 75%, temperatures may dip slightly as cloud '
                'cover reduces solar heating, and pressure often fluctuates with passing storm '
                'systems. After the monsoon withdraws in October, humidity drops, skies clear, '
                'and the sensor records Nepal\'s famously pleasant autumn weather.\n\n'
                'The relationship between the monsoon and Nepali society is deep. The rice '
                'planting calendar is set by monsoon onset. The festival of Ropain (paddy '
                'transplanting) is a community celebration tied directly to soil moisture '
                'reaching planting conditions. Water mills, irrigation canals and the entire '
                'architecture of hill agriculture are designed around the monsoon\'s rhythm.'
            ),
            'teacher_notes': (
                'If the session falls outside monsoon season, use the historical chart data '
                'available in the dashboard to show the contrast. Ask students to imagine being '
                'a farmer: how would they feel watching humidity rise in early June? What about '
                'watching it remain low through July in a drought year? The emotional and '
                'economic stakes of meteorological data are a key insight at this level.'
            ),
            'live_sensors': ['air_temp', 'air_hum'],
            'materials': ['Graph paper or printed chart', 'Calculator'],
            'procedure': [
                'Open the dashboard temperature and humidity history charts. What season are we currently in?',
                'Record the last 10 data points for temperature and humidity in a table.',
                'Calculate the mean (average) temperature and mean humidity from your 10 readings.',
                'Sketch a line graph of humidity over the 10 time points. Label the axes.',
                'In small groups, discuss: based on these readings, is this station currently in monsoon conditions? List three pieces of evidence from the data.',
                'Read the Nepal context above. List THREE ways the monsoon arrival matters to a Nepali farmer in the hills.',
                'Write a paragraph predicting what the humidity graph would look like from June to November.',
            ],
            'discussion_questions': [
                'Why might a delayed monsoon be economically devastating for a farming family in Sindhupalchok?',
                'Climate change is predicted to make monsoon rainfall more intense but less predictable. What does "more intense but less predictable" mean for farmers?',
                'Can you think of a festival or cultural practice in your own community that is tied to the seasons or weather?',
            ],
            'worksheet_questions': [
                {
                    'q': 'From your 10 data points, calculate: Mean temperature = ___ °C   Mean humidity = ___ %   Show your working.',
                    'answer_guide': 'Check arithmetic. Students should sum values and divide by 10.',
                    'marks': 4,
                },
                {
                    'q': 'Describe what happens to temperature and humidity in Nepal as the monsoon arrives in June. Use the words "increases", "decreases" and "because".',
                    'answer_guide': 'Humidity increases significantly because moisture-laden air arrives from the Bay of Bengal. Temperature may decrease slightly or remain similar because cloud cover reduces direct solar heating, but feels hotter due to high humidity.',
                    'marks': 4,
                },
                {
                    'q': 'Why does Nepal receive so much more monsoon rain than a country at the same latitude in, say, North Africa?',
                    'answer_guide': 'Nepal is directly in the path of the South Asian monsoon driven by the Indian Ocean. The Himalayas force moist air upward (orographic lift), causing heavy rainfall. North Africa is shielded from ocean moisture by distance and atmospheric circulation patterns.',
                    'marks': 4,
                },
                {
                    'q': 'Suggest ONE way a farmer could use a weather sensor like this one to make better farming decisions.',
                    'answer_guide': 'Accept reasonable answers: tracking soil drying after monsoon, deciding when to plant, monitoring temperature for frost risk at high altitude, identifying unusual drought conditions early.',
                    'marks': 2,
                },
            ],
            'vocabulary': [
                {'term': 'Monsoon', 'definition': 'A seasonal wind system that reverses direction between summer and winter, bringing wet summers to South Asia.'},
                {'term': 'Orographic Rainfall', 'definition': 'Rain caused when moist air is forced upward by mountains, cooling and releasing its moisture.'},
                {'term': 'Mean (Average)', 'definition': 'The sum of all values in a data set divided by the number of values.'},
                {'term': 'Time Series', 'definition': 'A sequence of data points recorded at successive points in time.'},
            ],
            'extension': (
                'Find a news article about a monsoon-related flood or drought event in Nepal in the '
                'last five years. Write a half-page analysis of how better sensor data networks '
                'across Nepal might have helped communities prepare for or respond to the event.'
            ),
            'curriculum_link': 'Nepal CDC Grade 8 Compulsory Science, Unit 4: Weather Phenomena; Grade 8 Mathematics, Unit 5: Statistics and Data',
            'sdg_links': ['SDG 2: Zero Hunger', 'SDG 13: Climate Action', 'SDG 11: Sustainable Communities'],
            'cross_curricular': [
                'Mathematics: Mean, graphing, time-series data',
                'Social Studies: Nepal\'s agricultural calendar, festivals tied to seasons',
                'Economics: Impact of rainfall variability on food security and livelihoods',
            ],
        },

        {
            'id': 'climate-03',
            'title': 'Pressure, Altitude, and Nepal\'s Diversity',
            'subtitle': 'Using a formula to turn pressure into elevation — and what elevation means for life',
            'grade_band': '9–10',
            'subjects': ['Physics', 'Geography', 'Mathematics'],
            'duration': '45 min',
            'type': 'experiment',
            'overview': (
                'Students derive the altitude of the sensor station from live barometric pressure '
                'data using the barometric formula, then explore how altitude shapes temperature, '
                'oxygen availability, biodiversity and human culture across Nepal\'s vertical landscape.'
            ),
            'nepal_context': (
                'In almost no other country on Earth can you travel from tropical lowlands to '
                'arctic summits in a single day. Nepal compresses ecological zones that span '
                'thousands of kilometres horizontally in most countries into a vertical band '
                'of 8,800 metres. This altitude diversity is not just scenery — it determines '
                'which crops grow where, why Sherpas have evolved higher red blood cell counts, '
                'why cooking takes longer at altitude (lower boiling point of water), and why '
                'Nepal\'s biodiversity is extraordinary despite its small land area.'
            ),
            'learning_objectives': [
                'Apply the barometric formula to calculate altitude from atmospheric pressure.',
                'Explain why pressure decreases with altitude in terms of the weight of air.',
                'Describe the relationship between altitude and temperature using the lapse rate.',
                'Analyse how altitude shapes ecosystems, agriculture and human physiology in Nepal.',
            ],
            'background': (
                'The barometric formula describes how atmospheric pressure changes with altitude. '
                'In simplified form: Altitude (m) = 44,330 × [1 − (P/P₀)^0.1903], where P is '
                'the measured pressure and P₀ = 1,013.25 hPa is the standard sea-level reference '
                'pressure. Our sensor hub already computes this for you — but understanding the '
                'formula means understanding why the relationship works.\n\n'
                'Pressure falls with altitude because there is simply less air above you. At sea '
                'level, the entire atmosphere presses down on you. At 5,000 m, about half the '
                'atmosphere is below you, so pressure is roughly half of sea-level pressure '
                '(about 540 hPa). At the summit of Everest (8,849 m), pressure is only about '
                '33% of sea-level pressure — which is why supplemental oxygen is required for '
                'most climbers.\n\n'
                'Temperature also falls with altitude — on average 6.5°C per 1,000 m, known as '
                'the environmental lapse rate. This means a location at 3,000 m will be roughly '
                '19.5°C cooler than a location at sea level, all else being equal. Combined with '
                'lower pressure and reduced oxygen partial pressure, this makes high altitude '
                'environments profoundly different from the lowlands.'
            ),
            'teacher_notes': (
                'The formula itself may be unfamiliar — focus on what each part means rather than '
                'deriving it from first principles. The key insight is that P/P₀ is a ratio '
                '(how much of sea-level pressure do we have?), and the exponent 0.1903 captures '
                'how the atmosphere is not a uniform column but thins as you go higher. A good '
                'check: if the sensor reads about 866 hPa, students should calculate roughly '
                '1,200–1,300 m altitude, which is consistent with a hill-region station in Nepal.'
            ),
            'live_sensors': ['pressure', 'altitude', 'air_temp'],
            'materials': ['Calculator', 'Graph paper', 'Map of Nepal showing elevation zones (optional)'],
            'procedure': [
                'Read the current pressure value from the sensor hub: P = ___ hPa',
                'Using the formula Altitude = 44,330 × [1 − (P ÷ 1013.25)^0.1903], calculate the estimated altitude of this station. Show your working.',
                'Compare your calculated altitude with the displayed altitude on the dashboard. Are they the same? If not, why might they differ?',
                'Note the current air temperature: T = ___ °C. Using the lapse rate of 6.5°C per 1,000 m, estimate what the air temperature would be at sea level right now.',
                'Look up (or estimate) the altitude of: (a) Kathmandu (b) Lukla airport (c) Everest Base Camp (d) Namche Bazaar. Calculate the expected pressure at each location.',
                'Draw a table with columns: Location | Altitude (m) | Expected Pressure (hPa) | Expected Temp if today\'s sea-level temp is X°C. Fill it in for the four locations.',
            ],
            'discussion_questions': [
                'Water boils at 100°C at sea level. At altitude, it boils at a lower temperature. Why might this matter for cooking rice or making noodles at a high-altitude teahouse?',
                'Sherpa communities have lived at altitude for generations. What physiological adaptations would help them thrive where others struggle? How might these show up in medical measurements?',
                'A village relocates from 800 m to 2,500 m to escape flooding. What changes would the inhabitants notice in their daily lives within the first week?',
            ],
            'worksheet_questions': [
                {
                    'q': 'Show your full calculation for the altitude of this station from today\'s pressure reading. P = ___ hPa. Calculated altitude = ___ m.',
                    'answer_guide': 'Check arithmetic. At 866 hPa, altitude ≈ 1,289 m. Accept ±50 m for rounding. Full marks for showing all steps.',
                    'marks': 5,
                },
                {
                    'q': 'Explain in TWO sentences why atmospheric pressure is lower at the top of a mountain than at sea level.',
                    'answer_guide': 'There is less air above you at higher altitude, so the total weight of the air column pressing down is less. Pressure is created by the weight of air, so less air above = lower pressure.',
                    'marks': 3,
                },
                {
                    'q': 'A climber at Everest Base Camp (5,364 m) has a pressure reading of approximately 505 hPa. What percentage of sea-level pressure is this? Why does this make breathing difficult?',
                    'answer_guide': '505 ÷ 1013.25 × 100 = 49.8% — roughly half. This means oxygen partial pressure is also about half of sea level, so each breath delivers roughly half as much oxygen to the blood.',
                    'marks': 4,
                },
            ],
            'vocabulary': [
                {'term': 'Barometric Formula', 'definition': 'A mathematical equation relating atmospheric pressure to altitude above sea level.'},
                {'term': 'Lapse Rate', 'definition': 'The rate at which air temperature decreases with altitude; on average 6.5°C per 1,000 m.'},
                {'term': 'Hectopascal (hPa)', 'definition': 'The unit of atmospheric pressure; 1 hPa = 100 Pascals. Standard sea-level pressure is 1,013.25 hPa.'},
                {'term': 'Orographic Effect', 'definition': 'The influence of mountains on local weather, including forced uplift of air masses and rain shadows.'},
            ],
            'extension': (
                'Research the concept of the "Death Zone" above 8,000 m. Write a scientific '
                'explanation of why the human body cannot acclimatise above this altitude, '
                'using pressure and oxygen partial pressure in your answer.'
            ),
            'curriculum_link': 'Nepal CDC Grade 9 Physics, Unit 5: Pressure; Grade 9 Geography, Unit 1: Physical Geography of Nepal',
            'sdg_links': ['SDG 13: Climate Action', 'SDG 15: Life on Land'],
            'cross_curricular': [
                'Mathematics: Powers and exponents, percentage calculations',
                'Biology: Human physiology at altitude, biodiversity across elevation zones',
                'Geography: Nepal\'s ecological zones, settlement patterns',
            ],
        },

        {
            'id': 'climate-04',
            'title': 'Nepal\'s Climate Story: Data, Change and Justice',
            'subtitle': 'Long-term readings, global patterns, and the ethics of a crisis Nepal did not cause',
            'grade_band': '11–12',
            'subjects': ['Environmental Science', 'Economics', 'Ethics', 'English'],
            'duration': '60 min',
            'type': 'discussion',
            'overview': (
                'Students analyse the station\'s historical temperature trend, compare it to '
                'regional climate projections, calculate the economic cost of climate impacts '
                'on Nepal, and engage with the ethical question of climate justice.'
            ),
            'nepal_context': (
                'Nepal emits less than 0.1% of global greenhouse gases, yet it is consistently '
                'ranked among the ten most climate-vulnerable nations on Earth. The Hindu Kush '
                'Himalayan glaciers — the "third pole" — are retreating at an accelerating rate, '
                'threatening the dry-season river flows that irrigate lowland farms and supply '
                'drinking water to tens of millions. Glacial Lake Outburst Floods (GLOFs) are '
                'increasing. Monsoon patterns are shifting. Extreme heat events in the Terai '
                'are becoming more frequent. This is not a future risk — it is already changing '
                'how Nepalis live, farm and plan their lives.'
            ),
            'learning_objectives': [
                'Extract a trend from time-series sensor data and represent it quantitatively.',
                'Explain Nepal\'s climate vulnerability in terms of both physical geography and economic exposure.',
                'Evaluate the concept of climate justice — who bears responsibility when the victims and the causes are different nations.',
                'Construct a structured written argument on a climate policy question.',
            ],
            'background': (
                'Climate change is not uniform — it affects different regions differently. '
                'The Hindu Kush Himalayan region is warming at roughly twice the global average '
                'rate. A 2°C global average warming means closer to 4°C in mountain areas. '
                'This is already measurable: the Himalayan glacier Ama Dablam\'s ice field '
                'has visibly retreated in photographs taken just decades apart. IPCC projections '
                'for South Asia show increased frequency of extreme rainfall events, longer dry '
                'spells between monsoon rains, and rising sea levels threatening coastal Bangladesh '
                '— which in turn drives migration pressure into Nepal.\n\n'
                'The economics of climate impact in Nepal are staggering relative to the country\'s '
                'GDP. The 2015 earthquake caused losses equivalent to about 35% of GDP; major '
                'flood-and-landslide years routinely cost 1–2% of GDP in infrastructure damage '
                'alone, not counting agricultural losses or health costs. The World Bank estimates '
                'that without adaptation investment, climate change could reduce Nepal\'s GDP by '
                '2–3% annually by 2050.\n\n'
                'Climate justice asks a fundamental question: if the countries that caused climate '
                'change are largely wealthy nations that industrialised over 150 years, and the '
                'countries experiencing the worst impacts are mostly poor nations that did very '
                'little to cause it, what are the moral obligations of wealthy nations to Nepal? '
                'This debate sits at the heart of every COP (Conference of Parties) climate '
                'negotiation, and Nepal\'s negotiators are active participants.'
            ),
            'teacher_notes': (
                'The discussion question around climate justice can become politically charged. '
                'Ground it in evidence: emissions per capita data, Nepal\'s own emissions profile, '
                'and the measurable impacts described in IPCC reports. The goal is not to reach a '
                'single political conclusion but to reason carefully about responsibility, '
                'causation and obligation. English teachers may wish to use the written argument '
                'task as a formal assessment piece.'
            ),
            'live_sensors': ['air_temp', 'pressure', 'altitude'],
            'materials': ['Access to dashboard historical chart', 'Calculator', 'Writing materials'],
            'procedure': [
                'Open the temperature history chart. Describe the trend you see in the data: is temperature increasing, decreasing, stable, or variable?',
                'Read: Nepal\'s average temperature has increased by approximately 0.06°C per year since 1975 — roughly double the global average rate. How much total warming does this imply over 50 years?',
                'In groups: list THREE specific ways this warming rate would affect (a) a Himalayan glacier, (b) a rice farmer in Chitwan, (c) a trekking tourism business.',
                'Calculate: if Nepal\'s annual GDP is approximately USD 40 billion, and climate damages are estimated at 2% of GDP annually by 2050, what is the annual financial loss in USD?',
                'Read Nepal\'s per-capita CO₂ emissions: approximately 0.5 tonnes per year per person. The global average is 4.7 tonnes. The USA average is 14.9 tonnes. Create a simple bar chart of these three values.',
                'Class debate or structured discussion: "Wealthy industrialised nations have a legal and moral obligation to fund Nepal\'s climate adaptation." Prepare two arguments for and two arguments against.',
            ],
            'discussion_questions': [
                'Is it fair that Nepal faces severe climate impacts from emissions it did not produce? How should fairness be defined in a global context?',
                'What is the difference between climate mitigation (reducing emissions) and climate adaptation (adjusting to impacts)? Which should Nepal prioritise, and who should pay for each?',
                'How would you feel if you were a Nepali negotiator at a COP summit, presenting these statistics to countries with 30× Nepal\'s per capita emissions?',
            ],
            'worksheet_questions': [
                {
                    'q': 'At 0.06°C of warming per year, how much warmer will Nepal be in 2075 compared to 2025? Show your calculation.',
                    'answer_guide': '2075 − 2025 = 50 years. 50 × 0.06 = 3.0°C warmer. Accept full marks for correct arithmetic and working shown.',
                    'marks': 3,
                },
                {
                    'q': 'Write a paragraph explaining why Nepal is particularly vulnerable to climate change despite having very low emissions. Include at least THREE specific physical or economic factors.',
                    'answer_guide': 'Should include: mountain glacier dependence for water; monsoon agriculture dependence; poverty limiting adaptation capacity; Himalayan warming amplification; GLOF risk; thin disaster-response capacity. Award marks for specificity.',
                    'marks': 6,
                },
                {
                    'q': 'Define "climate justice" in your own words and give one example of how it applies to Nepal\'s situation.',
                    'answer_guide': 'Climate justice is the principle that the burden of climate impacts should not fall disproportionately on those who contributed least to the problem. Nepal example: Nepal contributes <0.1% of emissions but faces GDP-scale losses from climate impacts caused primarily by wealthy industrialised nations.',
                    'marks': 4,
                },
            ],
            'vocabulary': [
                {'term': 'GLOF', 'definition': 'Glacial Lake Outburst Flood — a sudden release of water from a lake dammed by glacial ice or moraine, which can be catastrophic downstream.'},
                {'term': 'Climate Justice', 'definition': 'The ethical framework that considers the unequal causes and impacts of climate change across different nations, communities and generations.'},
                {'term': 'GDP', 'definition': 'Gross Domestic Product — the total monetary value of all goods and services produced in a country in a year.'},
                {'term': 'Climate Adaptation', 'definition': 'Changes made to human systems and practices to reduce harm from climate change impacts that are already occurring.'},
                {'term': 'Nationally Determined Contribution (NDC)', 'definition': 'A country\'s self-set plan under the Paris Agreement describing its climate commitments for emissions reduction and adaptation.'},
            ],
            'extension': (
                'Read Nepal\'s most recent Nationally Determined Contribution (NDC) submitted to '
                'the UNFCCC (available online). Identify two specific commitments Nepal has made '
                'and assess whether the data from a sensor station like this one could help '
                'monitor progress toward those commitments.'
            ),
            'curriculum_link': 'Nepal CDC Grade 11 Environmental Science, Unit 5: Climate Change and Sustainability; Grade 11 Economics, Unit 6: Development and Environment',
            'sdg_links': ['SDG 13: Climate Action', 'SDG 10: Reduced Inequalities', 'SDG 1: No Poverty', 'SDG 16: Peace, Justice and Strong Institutions'],
            'cross_curricular': [
                'Economics: GDP, development, cost of natural disasters',
                'English: Structured argument writing, policy brief format',
                'History: Nepal\'s environmental history, industrialisation and emissions',
                'Philosophy: Ethics of global responsibility and intergenerational equity',
            ],
        },

        {
            'id': 'climate-05',
            'title': 'Microclimate Monitoring as Scientific Practice',
            'subtitle': 'From single station to publishable dataset — rigour, uncertainty and contribution',
            'grade_band': 'UG',
            'subjects': ['Environmental Science', 'Research Methods', 'Statistics'],
            'duration': '90 min',
            'type': 'research',
            'overview': (
                'Undergraduate students design a formal monitoring study using the sensor hub, '
                'grapple with calibration uncertainty, compare their readings to reanalysis '
                'data, and understand what it means to contribute to an open scientific record.'
            ),
            'nepal_context': (
                'Nepal has one of the thinnest meteorological observation networks of any country '
                'in the world — fewer than 400 official weather stations for a country of diverse '
                'terrain spanning huge altitude ranges. High mountain stations are sparse and '
                'expensive to maintain. This data gap directly limits climate science in the '
                'region. Community-owned sensor stations of exactly this type are increasingly '
                'recognised in the scientific literature as a way to fill these gaps — but only '
                'if the data is collected with appropriate rigour, documented transparently, '
                'and shared openly.'
            ),
            'learning_objectives': [
                'Design a measurement protocol specifying sampling frequency, logging duration and quality control procedures.',
                'Quantify uncertainty in sensor measurements from known specifications and environmental sources.',
                'Compare station data with ERA5 reanalysis gridded data and explain discrepancies.',
                'Write a data methods section meeting the standard expected in an environmental science paper.',
            ],
            'background': (
                'A single sensor reading is not the same as scientific data. Scientific data '
                'requires documentation of instrument specifications, calibration status, '
                'measurement uncertainty, site metadata (location, altitude, land cover, '
                'nearby heat sources) and a quality-control procedure for flagging or removing '
                'anomalous readings. Without this documentation, a dataset cannot be critically '
                'evaluated by others or compared to data from different stations.\n\n'
                'ERA5 is the European Centre for Medium-Range Weather Forecasts (ECMWF) global '
                'atmospheric reanalysis — a model-derived dataset that blends historical '
                'observations with atmospheric models to produce gridded estimates of weather '
                'variables at approximately 31 km horizontal resolution for every hour since '
                '1940. It is freely available via the Copernicus Climate Data Store. Comparing '
                'your station\'s readings to ERA5 values for the same grid cell and time period '
                'is a standard way to check for systematic biases in low-cost sensors.\n\n'
                'Open data practices require that datasets be deposited in accessible repositories '
                'with persistent identifiers (DOIs), complete metadata, and clear licensing. '
                'The FAIR principles (Findable, Accessible, Interoperable, Reusable) are the '
                'current standard for research data management. The himalayansciences.org platform '
                'this hub can upload to is designed with these principles in mind.'
            ),
            'teacher_notes': (
                'This activity is best run as a multi-week project rather than a single session. '
                'The 90-minute session designs the study; data collection continues over 1–4 weeks; '
                'the analysis and writing phases follow. Assessment should focus on methodological '
                'rigour and the quality of the uncertainty analysis, not on "getting good results" '
                '— unexpected discrepancies between the station and ERA5 are valuable findings, '
                'not failures. Guide students toward explaining discrepancies rather than dismissing them.'
            ),
            'live_sensors': ['air_temp', 'air_hum', 'pressure', 'altitude'],
            'materials': ['Access to ERA5 via Copernicus CDS (internet required)', 'Spreadsheet software', 'GPS coordinates of station'],
            'procedure': [
                'Document the station metadata: GPS coordinates, altitude (sensor-derived and map-derived), surrounding land cover (forest / cropland / urban / other), distance to nearest building, sensor model and firmware version.',
                'Note the sensor specifications: temperature accuracy ±0.5°C, humidity accuracy ±2%, pressure accuracy ±1 hPa. Calculate the resulting altitude uncertainty using error propagation.',
                'Design a sampling protocol: decide on logging frequency (current: every 60s), data retention, and quality-control flags (e.g. flag readings where temperature changes >5°C in 60s as suspect).',
                'Access ERA5 data for the nearest grid point. Compare ERA5 2 m temperature and surface pressure to this station\'s readings for the same time period.',
                'Calculate the mean bias (station minus ERA5) and the root mean square error (RMSE) for temperature and pressure.',
                'Write a 400-word data methods section describing the station, instrumentation, sampling protocol and quality-control approach, following the structure of a published journal article.',
            ],
            'discussion_questions': [
                'ERA5 represents an average over a 31 km grid cell. Why might a single station always disagree with ERA5 to some degree, even if both are perfectly accurate?',
                'What would you need to do to this dataset before submitting it to a data repository? What metadata is essential?',
                'A journalist cites your station\'s temperature reading as evidence of a record-breaking heat event. What caveats would you want them to include?',
            ],
            'worksheet_questions': [
                {
                    'q': 'The BMP280 pressure sensor has a stated accuracy of ±1 hPa. Using error propagation through the barometric formula, estimate the resulting uncertainty in the calculated altitude in metres.',
                    'answer_guide': 'At ~866 hPa and 1,289 m, dA/dP ≈ −8.4 m/hPa. So uncertainty ≈ ±8.4 m. Accept answers in range ±5 to ±15 m with reasoning shown.',
                    'marks': 6,
                },
                {
                    'q': 'List THREE potential sources of systematic bias in a low-cost temperature sensor mounted inside a building or in direct sunlight.',
                    'answer_guide': 'Heat island effect from building; solar radiation heating sensor enclosure; insufficient ventilation around sensor; proximity to heat sources (computers, humans); ground radiation at night.',
                    'marks': 3,
                },
            ],
            'vocabulary': [
                {'term': 'Reanalysis Data', 'definition': 'A gridded climate dataset produced by combining historical observations with a weather model to create a continuous record with no gaps.'},
                {'term': 'Uncertainty', 'definition': 'The range within which the true value of a measurement is expected to lie, arising from limitations in instruments, methods and environmental conditions.'},
                {'term': 'FAIR Principles', 'definition': 'A framework for scientific data management: data should be Findable, Accessible, Interoperable and Reusable.'},
                {'term': 'Metadata', 'definition': 'Data that describes other data — in a sensor context, this includes location, instrument type, calibration status and measurement conditions.'},
            ],
            'extension': (
                'Submit a week of quality-controlled data to himalayansciences.org and write a '
                '200-word data note describing the station. Consider submitting this as a data '
                'paper to a student journal.'
            ),
            'curriculum_link': 'Undergraduate Environmental Science / Geography / Physics Research Methods courses; aligns with UGC Nepal research skills requirements',
            'sdg_links': ['SDG 13: Climate Action', 'SDG 17: Partnerships for the Goals', 'SDG 4: Quality Education'],
            'cross_curricular': [
                'Statistics: Error propagation, RMSE, bias calculation',
                'Computer Science: API access, data formats, database management',
                'English: Scientific writing — methods section, data note format',
            ],
        },

        {
            'id': 'climate-sky',
            'title': 'Cloud Spotting: Reading the Sky',
            'subtitle': 'Use the sky camera to identify cloud types and predict coming weather',
            'grade_band': '6–8',
            'subjects': ['Science', 'Geography'],
            'duration': '45 min',
            'type': 'observation',
            'viz_type': 'sky-cam',
            'viz_config': {'title': 'Live sky from this station — what do you see?'},
            'overview': (
                'Clouds are one of nature\'s most reliable weather forecasts. In this activity '
                'students observe the live sky camera feed, learn to identify the most common '
                'cloud types, and practice making short-range weather predictions from what they see. '
                'The activity connects Nepal\'s dramatic monsoon and dry seasons to the cloud patterns '
                'students can observe in real time.'
            ),
            'nepal_context': (
                'Nepal\'s sky tells a vivid seasonal story. During the pre-monsoon (April–May) '
                'towering cumulonimbus clouds build over the Himalaya by mid-afternoon, bringing '
                'heavy thunder and hail. The monsoon months (June–September) bring persistent '
                'stratus and nimbostratus cloud, reducing solar radiation by up to 70%. In the dry '
                'season (October–March) the sky is often a deep blue — minimal cloud, maximum solar '
                'radiation, bitter cold nights. A sky camera can capture these seasonal transitions '
                'over weeks and months.'
            ),
            'teacher_notes': (
                'The best way to run this activity is to let students observe the camera image first '
                'before introducing the classification system — note what they notice, what confuses them. '
                'Cloud cover % from the image analysis is a rough estimate; have students compare it '
                'to their own visual estimate. If the sky is clear, focus on sky colour changes through '
                'the day (blue → orange → dark) as a light-scattering lesson.'
            ),
            'live_sensors': ['air_temp', 'air_hum', 'pressure'],
            'materials': ['Sky camera (built in to this station)', 'Cloud identification chart (below)', 'Weather notebook'],
            'procedure': [
                'Look at the live sky camera image. Describe in words what you see — colour, texture, how much of the sky is covered.',
                'Estimate cloud cover as a fraction: 0/8 (clear) to 8/8 (overcast). Compare to the station\'s automated estimate in the panel above.',
                'Use the cloud type guide below to identify the main cloud type in the image. Record the name and altitude range.',
                'Read the barometric pressure sensor. Is pressure rising, steady, or falling? (Compare the current value to the value from 30 minutes ago on the dashboard chart.)',
                'Based on cloud type and pressure trend, write a one-sentence weather prediction for the next 6 hours.',
                'After 24 hours, revisit your prediction. Was it correct? What was the hardest part to predict?',
            ],
            'discussion_questions': [
                'Cumulus clouds look like fluffy cotton wool. What does their base height tell you about the lifting condensation level — the altitude at which rising air becomes saturated?',
                'During the monsoon, Nepal is often completely overcast for days. How does this affect agriculture, solar panels, and temperature? Who benefits from cloud cover? Who suffers?',
                'A fisheye lens gives a very wide view of the sky. What are the advantages and disadvantages compared to a standard narrow-angle camera for cloud observation?',
            ],
            'worksheet_questions': [
                {
                    'q': 'Match each cloud type to its typical altitude and weather association: Cumulus, Cirrus, Stratus, Cumulonimbus.',
                    'answer_guide': 'Cumulus: 500–2000m, fair weather; Cirrus: >6000m, high thin ice, weather change coming; Stratus: 0–2000m, grey overcast, drizzle; Cumulonimbus: 0–12000m, thunderstorm/heavy rain.',
                    'marks': 4,
                },
                {
                    'q': 'The station records 992 hPa and falling. Identify TWO cloud types you might expect to see and explain why.',
                    'answer_guide': 'Low pressure approaching → nimbostratus (grey, rain-bearing), or cumulonimbus if convective instability is present. Accept other reasonable types with valid explanation.',
                    'marks': 4,
                },
            ],
            'vocabulary': [
                {'term': 'Cloud Cover', 'definition': 'The fraction of the sky hidden by clouds, measured in eighths (oktas) from 0 (clear) to 8 (overcast).'},
                {'term': 'Cumulus', 'definition': 'Puffy, heap-like clouds with flat bases. Form when warm air rises, cools, and water vapour condenses.'},
                {'term': 'Cumulonimbus', 'definition': 'A massive storm cloud extending from near the surface to the tropopause. Associated with heavy rain, lightning and hail.'},
                {'term': 'Barometric Pressure', 'definition': 'The weight of the atmosphere pressing down on a surface. Falling pressure often signals approaching bad weather.'},
                {'term': 'Fisheye Lens', 'definition': 'A wide-angle lens with >100° field of view, allowing most of the sky hemisphere to be captured in a single image.'},
            ],
            'extension': (
                'Keep a 2-week sky diary: take daily screenshots of the camera image at the same time '
                'each day and note the weather that followed. Build a simple table correlating cloud type '
                'and pressure to observed weather outcomes.'
            ),
            'curriculum_link': 'Grade 6–8 Science (Nepal CDC): Weather and Climate; Earth\'s Atmosphere',
            'sdg_links': ['SDG 13: Climate Action', 'SDG 11: Sustainable Cities'],
            'cross_curricular': [
                'Geography: Weather systems, Nepal seasonal climate',
                'Mathematics: Fractions (oktas), data tables',
                'Art: Cloud sketching, sky colour observation',
            ],
        },
    ],
}
