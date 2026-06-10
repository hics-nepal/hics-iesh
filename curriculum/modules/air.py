AIR = {
    'id': 'air',
    'title': 'Air Quality & Health',
    'icon': '💨',
    'color': '#f0883e',
    'tagline': 'What we breathe — carbon monoxide, air quality and the health of Nepal\'s atmosphere',
    'description': (
        'Air quality is invisible but measurable, and its consequences for human health are '
        'profound. This module uses CO and air quality index sensors to explore the chemistry '
        'of combustion, Nepal\'s specific air pollution challenges, the health burden of '
        'indoor and outdoor pollution, and the social inequities in who breathes the worst air.'
    ),
    'sensors': ['mq7_raw', 'mq135_raw'],
    'teaching_guide': (
        'The MQ-7 and MQ-135 sensors in this hub provide relative readings — not calibrated '
        'ppm values. Be transparent with students about this: the sensors are useful for '
        'detecting change and relative levels, but should not be cited as precise ppm '
        'measurements without calibration. This is itself a valuable lesson about the '
        'difference between a sensor reading and a measurement. For health discussions, '
        'use published WHO data for specific pollutant thresholds rather than the raw sensor '
        'values. The Nepal context for air quality is particularly rich — bring in news '
        'articles about Kathmandu\'s air quality rankings and the experiences of communities '
        'that rely on biomass cooking fires.'
    ),
    'activities': [

        {
            'id': 'air-01',
            'title': 'Invisible Dangers in the Air',
            'subtitle': 'Understanding what the sensors detect and why it matters for health',
            'grade_band': '6–8',
            'subjects': ['Science', 'Health'],
            'duration': '30 min',
            'type': 'observation',
            'viz_type': 'hz-gauges',
            'viz_config': {
                'title': 'What does the air quality sensor detect right now?',
                'gauges': [
                    {
                        'key': 'mq7_raw', 'label': 'CO Level (MQ-7 sensor)', 'unit': 'sensor units',
                        'min': 0, 'max': 4095,
                        'zones': [
                            {'label': 'Low', 'color': '#3fb950', 'pct': 25},
                            {'label': 'Moderate', 'color': '#d29922', 'pct': 35},
                            {'label': 'High', 'color': '#f0883e', 'pct': 25},
                            {'label': 'Danger', 'color': '#f85149', 'pct': 15},
                        ],
                        'fact': 'CO is colourless and odourless — the sensor detects what your nose cannot.',
                    },
                    {
                        'key': 'mq135_raw', 'label': 'Mixed Gas / Air Quality (MQ-135)', 'unit': 'sensor units',
                        'min': 0, 'max': 4095,
                        'zones': [
                            {'label': 'Good', 'color': '#3fb950', 'pct': 20},
                            {'label': 'Moderate', 'color': '#d29922', 'pct': 30},
                            {'label': 'Poor', 'color': '#f0883e', 'pct': 30},
                            {'label': 'Hazardous', 'color': '#f85149', 'pct': 20},
                        ],
                        'fact': 'MQ-135 detects smoke, CO₂, benzene and ammonia — common indoor cooking pollutants.',
                    },
                ],
            },
            'overview': (
                'Students take their first air quality readings, learn what CO and mixed gases '
                'mean for health, and identify common sources of air pollution in Nepali homes '
                'and communities.'
            ),
            'nepal_context': (
                'In Nepal, approximately 70% of households still cook with biomass fuels — wood, '
                'crop residues and animal dung. This produces a mixture of carbon monoxide, '
                'particulates and other harmful gases inside homes, particularly in kitchens '
                'without chimneys. The World Health Organization estimates that household air '
                'pollution from solid fuel cooking kills approximately 13,000 Nepalis annually — '
                'mostly women and young children who spend the most time near cooking fires. '
                'This is not a distant urban problem or a factory issue — it is happening in '
                'millions of Nepali kitchens every day.'
            ),
            'learning_objectives': [
                'Identify carbon monoxide (CO) as a product of incomplete combustion and explain why it is dangerous.',
                'Read relative air quality sensor values and describe what changes in those values might indicate.',
                'List common sources of indoor and outdoor air pollution in Nepal.',
                'Explain the link between cooking fuel type and respiratory health.',
            ],
            'background': (
                'Carbon monoxide (CO) is a colourless, odourless gas produced whenever carbon-containing '
                'materials burn without sufficient oxygen. This "incomplete combustion" happens in '
                'wood fires, charcoal stoves, vehicle engines and burning crop waste. CO is dangerous '
                'because it binds to haemoglobin in the blood 200 times more strongly than oxygen, '
                'preventing blood from carrying oxygen to organs. Even low concentrations cause '
                'headaches, dizziness and fatigue; high concentrations cause death.\n\n'
                'The MQ-135 sensor detects a range of gases including ammonia (from animal waste '
                'and fertiliser), CO₂ (from breathing and combustion), benzene and other volatile '
                'organic compounds. It gives a single "air quality" reading rather than '
                'identifying individual gases. Both sensors produce a higher raw ADC value when '
                'gas concentrations increase — but the readings require calibration against known '
                'gas concentrations to convert to ppm (parts per million).\n\n'
                'Nepal\'s air quality challenges span indoor and outdoor environments. In Kathmandu '
                'valley, trapped by surrounding hills and filled with vehicle exhaust, brick kiln '
                'smoke and dust from rapid construction, the valley regularly ranks among South '
                'Asia\'s most polluted urban areas in winter. In rural areas, the main threat is '
                'indoor pollution from cooking. Both contexts are important, and both show up — '
                'in different ways — in sensor readings.'
            ),
            'teacher_notes': (
                'If your school allows it, a brief demonstration of CO generation is powerful: '
                'light a candle, hold the sensor briefly near (but not dangerously close to) '
                'the flame and observe the reading rise. Extinguish the candle and watch it fall. '
                'Never use this sensor to make health claims about specific spaces — the '
                'uncalibrated readings are relative indicators only. Emphasise that the sensor '
                'shows change, not absolute concentration.'
            ),
            'live_sensors': ['mq7_raw', 'mq135_raw'],
            'materials': ['Notebook', 'Candle (optional, for demonstration only)'],
            'procedure': [
                'Read the current MQ-7 (CO) and MQ-135 (air quality) raw values from the dashboard. Record them.',
                'The bar next to each reading shows how high the value is relative to the maximum (4095). What percentage of maximum is each reading at?',
                'Open a window or door if possible. Wait 5 minutes. Do the readings change? Why might fresh air affect the values?',
                'Brainstorm as a class: list 5 sources of air pollution inside a typical Nepali home and 5 sources outside.',
                'For each source, predict whether it would affect the MQ-7 reading, the MQ-135 reading, or both.',
                'Read the Nepal context above. Calculate: if 13,000 people die per year from household air pollution, how many is that per day? Per hour?',
            ],
            'discussion_questions': [
                'Why is carbon monoxide particularly dangerous compared to other pollutants — even though you can\'t see or smell it?',
                'Women and young children in Nepal are most affected by indoor air pollution. Why?',
                'What changes to a kitchen design could reduce indoor air pollution from a wood cooking fire?',
            ],
            'worksheet_questions': [
                {
                    'q': 'Record MQ-7 reading: ___ and MQ-135 reading: ___ . Calculate each as a percentage of the maximum 4095.',
                    'answer_guide': 'Check arithmetic: (reading ÷ 4095) × 100. Values around 5–15% are typical in clean indoor air.',
                    'marks': 3,
                },
                {
                    'q': 'Explain in three sentences why carbon monoxide is dangerous to humans, even in small amounts.',
                    'answer_guide': 'CO is colourless and odourless so you cannot detect it. It binds to haemoglobin in blood 200× more strongly than oxygen. This prevents blood from carrying oxygen to the brain and organs, causing illness or death.',
                    'marks': 3,
                },
                {
                    'q': 'Name THREE sources of indoor air pollution common in Nepal and suggest one practical way to reduce indoor pollution in a rural Nepali kitchen.',
                    'answer_guide': 'Sources: wood fire cooking, burning incense, kerosene lamps, animal dung fuel, smoking. Solutions: improved cookstoves with chimneys, switching to LPG or biogas, opening windows and doors, cross-ventilation in kitchen design.',
                    'marks': 4,
                },
            ],
            'vocabulary': [
                {'term': 'Carbon Monoxide (CO)', 'definition': 'A colourless, odourless toxic gas produced by incomplete combustion of carbon-containing fuels.'},
                {'term': 'Incomplete Combustion', 'definition': 'Burning that occurs with insufficient oxygen, producing CO and soot rather than CO₂ and water.'},
                {'term': 'Haemoglobin', 'definition': 'The protein in red blood cells that carries oxygen from the lungs to the rest of the body.'},
                {'term': 'Indoor Air Pollution', 'definition': 'Contamination of the air inside buildings, most commonly from cooking fires, heating and cleaning products.'},
            ],
            'extension': (
                'Research "improved cookstove" programmes in Nepal. Find one organisation working '
                'on this and write a 150-word summary of their approach, who they target, and '
                'what evidence they have for health improvements.'
            ),
            'curriculum_link': 'Nepal CDC Grade 7 Compulsory Science, Unit 6: Air and Its Properties; Grade 7 Health Education, Unit 2: Environmental Health',
            'sdg_links': ['SDG 3: Good Health and Well-Being', 'SDG 7: Affordable and Clean Energy', 'SDG 11: Sustainable Cities and Communities'],
            'cross_curricular': [
                'Health: Respiratory diseases, effects of indoor pollution',
                'Mathematics: Percentage calculation, rate (deaths per day)',
                'Social Studies: Cooking practices and fuel use in Nepal',
            ],
        },

        {
            'id': 'air-02',
            'title': 'Nepal\'s Air Quality Crisis',
            'subtitle': 'From valley smog to hill fires — mapping the geography and causes of air pollution',
            'grade_band': '8–10',
            'subjects': ['Geography', 'Health', 'Social Studies'],
            'duration': '45 min',
            'type': 'analysis',
            'overview': (
                'Students analyse air quality patterns, investigate the specific causes of '
                'Nepal\'s urban and rural air pollution, and assess its health and economic '
                'burden using real data alongside sensor readings.'
            ),
            'nepal_context': (
                'Kathmandu Valley\'s air quality regularly exceeds WHO safe limits. In winter '
                'and spring — when cold air traps pollution at low altitude in the bowl-shaped '
                'valley and farmers in the surrounding hills burn crop residues — particulate '
                'matter (PM2.5) levels can reach 10–15× the WHO guideline of 15 µg/m³. Nepal\'s '
                'brick kilns, which supply construction materials for a rapidly urbanising '
                'country, are a major source of black carbon and CO. In rural areas, spring '
                'burning of agricultural residue in the Terai creates smoke plumes visible from '
                'satellite imagery. There is no single cause and no simple solution.'
            ),
            'learning_objectives': [
                'Explain why Kathmandu Valley is particularly vulnerable to air pollution concentration.',
                'Identify and categorise the main sources of air pollution in Nepal by sector.',
                'Interpret the air quality index (AQI) scale and relate it to health effects.',
                'Analyse the disproportionate health burden of air pollution across socioeconomic groups.',
            ],
            'background': (
                'Air pollution consists of gases (CO, NO₂, SO₂, ozone) and particles (PM10 and '
                'PM2.5, where the number refers to diameter in micrometres). PM2.5 — particles '
                'smaller than 2.5 µm — is considered the most dangerous because its tiny size '
                'allows it to penetrate deep into the lungs and enter the bloodstream. Sources '
                'in Nepal include vehicle exhaust (mostly old, poorly maintained diesel vehicles), '
                'brick kilns (operating a traditional Bull\'s Trench design rather than cleaner '
                'zigzag kilns), biomass burning, road dust and industrial activity.\n\n'
                'Kathmandu\'s geography makes it especially prone to pollution accumulation. The '
                'valley sits at 1,400 m, surrounded by hills rising to 2,700 m on three sides. '
                'In winter, a temperature inversion forms — warm air sits above cold trapped air '
                'in the valley, acting like a lid that prevents vertical mixing. Pollutants '
                'accumulate in the trapped cold layer. This is the same meteorological mechanism '
                'responsible for the 1952 Great London Smog, which killed 4,000 people in four days.\n\n'
                'Nepal\'s Department of Environment conducts air quality monitoring at a small '
                'number of stations. IQ Air\'s global ranking has placed Kathmandu among the '
                'world\'s 20 most polluted capitals in multiple recent years. The health cost '
                'is real: respiratory diseases, cardiovascular disease, low birth weight and '
                'reduced cognitive development in children are all linked to chronic PM2.5 exposure.'
            ),
            'teacher_notes': (
                'A good entry point for this activity is asking students what the air smells like '
                'on a winter morning in Kathmandu versus a monsoon morning — or asking those '
                'who have visited Kathmandu to describe what they see. Connecting the global '
                'framework (AQI, WHO guidelines) to local experience grounds the statistics in '
                'reality. The temperature inversion mechanism is also excellent for reinforcing '
                'atmospheric concepts from the Climate module.'
            ),
            'live_sensors': ['mq7_raw', 'mq135_raw'],
            'materials': ['AQI reference table (provided below)', 'Map of Kathmandu Valley (optional)'],
            'procedure': [
                'Record today\'s MQ-7 and MQ-135 readings and note the time of day and current weather conditions.',
                'Study the AQI reference table: Good (0–50), Moderate (51–100), Unhealthy for Sensitive Groups (101–150), Unhealthy (151–200), Very Unhealthy (201–300), Hazardous (301+).',
                'Research: what was Kathmandu\'s PM2.5 AQI on the worst day recorded in the last 5 years? What were people advised to do?',
                'List the FIVE main sources of air pollution in Nepal. For each, categorise it as: (a) indoor or outdoor, (b) urban or rural, (c) seasonal or year-round.',
                'Draw a simple diagram showing why cold air is trapped in Kathmandu Valley in winter (temperature inversion). Label: warm air layer, cold air layer, pollution trapped, valley walls.',
                'Calculate: if average Kathmandu PM2.5 is 50 µg/m³ and the WHO guideline is 15 µg/m³, by what percentage does Kathmandu exceed the guideline?',
            ],
            'discussion_questions': [
                'Poor families in Nepal are more likely to use biomass fuels, live near roads or brick kilns, and have less access to healthcare. How does air pollution become a poverty issue?',
                'Should the Nepali government prioritise reducing Kathmandu\'s outdoor pollution or Nepal\'s rural indoor pollution? What criteria would guide this decision?',
                'A school in Kathmandu is considering installing an air quality sensor in each classroom. What would the data be used for? What decisions could it inform?',
            ],
            'worksheet_questions': [
                {
                    'q': 'Explain in your own words what a "temperature inversion" is and why it causes pollution to concentrate in Kathmandu Valley.',
                    'answer_guide': 'A temperature inversion occurs when a layer of warm air sits above cooler air near the ground. Normally warm air rises (convection), mixing pollutants upward and dispersing them. An inversion acts as a lid — pollutants accumulate in the trapped cold layer and cannot escape. Kathmandu\'s surrounding hills prevent horizontal dispersal as well.',
                    'marks': 5,
                },
                {
                    'q': 'Calculate: If Kathmandu\'s average PM2.5 concentration is 50 µg/m³, how many times higher is it than the WHO annual guideline of 5 µg/m³?',
                    'answer_guide': '50 ÷ 5 = 10 times higher than the WHO annual guideline. (Note: the 24-hour guideline is 15 µg/m³, which would give 50 ÷ 15 = 3.3 times. Accept either with correct calculation.)',
                    'marks': 2,
                },
                {
                    'q': 'Explain why women and children in rural Nepal face a higher health risk from air pollution than adult men in the same household.',
                    'answer_guide': 'Women spend more time cooking near the fire; children spend time in the kitchen. Both are exposed to indoor smoke for many hours daily. Adult men often work outside away from the kitchen. Additionally, children\'s developing lungs are more vulnerable to PM2.5 damage than adult lungs.',
                    'marks': 4,
                },
            ],
            'vocabulary': [
                {'term': 'PM2.5', 'definition': 'Particulate matter with diameter less than 2.5 micrometres — fine particles that can penetrate deep into the lungs and enter the blood.'},
                {'term': 'Temperature Inversion', 'definition': 'An atmospheric condition where a layer of warm air sits above cooler air, trapping pollutants near the ground.'},
                {'term': 'Air Quality Index (AQI)', 'definition': 'A numerical scale from 0 to 500 that translates complex pollution measurements into a single indicator of health risk.'},
                {'term': 'Black Carbon', 'definition': 'Fine particles from incomplete combustion of carbon fuels; a major component of soot, a potent short-lived climate pollutant and health hazard.'},
            ],
            'extension': (
                'Access real-time Nepal air quality data from IQ Air (iqair.com) or Nepal\'s '
                'Department of Environment portal. Compare today\'s Kathmandu AQI to the '
                'reading from our station. Write a paragraph explaining what accounts for '
                'any difference between the two readings.'
            ),
            'curriculum_link': 'Nepal CDC Grade 8 Geography, Unit 4: Environmental Problems; Grade 9 Health Education, Unit 5: Environmental Health',
            'sdg_links': ['SDG 3: Good Health and Well-Being', 'SDG 11: Sustainable Cities', 'SDG 13: Climate Action'],
            'cross_curricular': [
                'Mathematics: Percentage calculations, ratio, data interpretation',
                'Geography: Kathmandu valley geography, urban vs rural Nepal',
                'Health: Respiratory disease, health equity, burden of disease',
                'Social Studies: Poverty, inequality and environmental risk',
            ],
        },

        {
            'id': 'air-03',
            'title': 'The Chemistry of What We Breathe',
            'subtitle': 'Combustion reactions, sensor physics and the molecular basis of air quality',
            'grade_band': '9–10',
            'subjects': ['Chemistry', 'Physics'],
            'duration': '45 min',
            'type': 'experiment',
            'overview': (
                'Students write and balance combustion equations, learn how MQ sensors detect '
                'gases through electrical resistance changes, and connect chemistry theory to '
                'live sensor readings from the device.'
            ),
            'nepal_context': (
                'Nepal\'s transition from biomass fuels to cleaner alternatives — LPG, biogas '
                'and increasingly solar electric cooking — is fundamentally a question of '
                'combustion chemistry. A wood fire and a clean LPG burner are both combustion '
                'reactions, but the completeness of combustion, the pollutants produced, and '
                'the energy efficiency differ dramatically. Understanding this chemistry is '
                'the foundation of any policy or personal decision about cooking fuel.'
            ),
            'learning_objectives': [
                'Write and balance chemical equations for complete and incomplete combustion of carbon fuels.',
                'Explain how metal oxide gas sensors detect gases through changes in electrical resistance.',
                'Interpret the voltage divider circuit used to protect the MCP3208 ADC from MQ sensor output.',
                'Relate chemical combustion theory to real sensor readings and Nepal\'s fuel transition.',
            ],
            'background': (
                'Combustion is a rapid oxidation reaction between a fuel and oxygen that releases '
                'energy as heat and light. For a simple carbon fuel in complete combustion: '
                'C + O₂ → CO₂ + energy. For incomplete combustion (insufficient oxygen): '
                '2C + O₂ → 2CO + energy. In a wood fire, both reactions occur — the ratio '
                'depends on oxygen availability, fire temperature and fuel moisture content. '
                'A well-stoked fire with good airflow produces mostly CO₂; a smouldering fire '
                'with wet wood produces CO and soot.\n\n'
                'MQ gas sensors work through a semiconductor principle. The sensing element is '
                'a ceramic tube coated with a metal oxide — typically tin dioxide (SnO₂). In '
                'clean air, oxygen molecules adsorb onto the surface of the SnO₂, creating a '
                'potential barrier that limits electron flow — the resistance is high. When a '
                'reducing gas like CO is present, it reacts with the adsorbed oxygen: '
                'CO + O⁻(ads) → CO₂ + e⁻. This releases an electron and lowers the resistance. '
                'The sensor circuit converts this resistance change to a voltage change, which '
                'the ADC reads as a higher numerical value.\n\n'
                'Our device uses a voltage divider before the ADC to protect it: two 4.7kΩ '
                'resistors halve the MQ output voltage from 0–5V to 0–2.5V, which is within '
                'the MCP3208\'s 3.3V reference range. This means the raw ADC values must be '
                'multiplied by 2 to get the true sensor output voltage — which is why the '
                'dashboard shows a "sensor voltage" field alongside the raw ADC reading.'
            ),
            'teacher_notes': (
                'The sensor physics section can be taught at different depths depending on class '
                'level. Grade 9 students can grasp the qualitative relationship (more gas → lower '
                'resistance → higher ADC reading) without the semiconductor band theory. Grade 10 '
                'and above can engage with the concept of adsorption and electron transfer. The '
                'voltage divider circuit is an excellent application of Ohm\'s law and Kirchhoff\'s '
                'voltage law that bridges chemistry and physics.'
            ),
            'live_sensors': ['mq7_raw', 'mq135_raw'],
            'materials': ['Periodic table', 'Calculator'],
            'procedure': [
                'Read current MQ-7 and MQ-135 raw ADC values and their displayed sensor voltages.',
                'Write the balanced equation for complete combustion of methane (CH₄ + O₂ → ?).',
                'Write the balanced equation for incomplete combustion of methane (CH₄ + insufficient O₂ → CO + H₂O). Balance it.',
                'Now write the complete and incomplete combustion equations for ethanol (C₂H₅OH), which is used in some cleaner cookstoves.',
                'The MQ-7 reads higher when CO concentration increases. Draw a circuit diagram showing: MQ sensor resistance (RS) + load resistor (RL, 1kΩ) + 5V supply + ADC input. Label where the ADC reads its voltage.',
                'Calculate: today\'s MQ-7 raw ADC = ___. Sensor voltage (ADC voltage × 2) = ___V. Sensor resistance RS = 1000 × (5V ÷ sensor_voltage − 1) = ___ Ω.',
            ],
            'discussion_questions': [
                'Why does a smouldering, oxygen-starved fire produce more CO than a hot, well-aerated flame? Relate this to the chemistry of combustion.',
                'Nepal is transitioning from wood cooking fires to LPG (liquefied petroleum gas, primarily propane C₃H₈). Write the balanced complete combustion equation for propane. Does this produce CO? Under what conditions might it?',
                'If a sensor reads higher when resistance is lower, what would happen to the MQ-7 reading inside a room with a running car engine? Why is this dangerous?',
            ],
            'worksheet_questions': [
                {
                    'q': 'Balance the following equation for incomplete combustion of butane (used in camping stoves): C₄H₁₀ + O₂ → CO + H₂O',
                    'answer_guide': '2C₄H₁₀ + 9O₂ → 8CO + 10H₂O. Check balancing: C: 8=8; H: 20=20; O: 18=18. Award marks for correct balancing even if student uses different integer multiples.',
                    'marks': 4,
                },
                {
                    'q': 'Explain the chain of events from a rise in CO concentration to a higher number on the MQ-7 ADC reading. Use the terms: reducing gas, metal oxide, resistance, voltage.',
                    'answer_guide': 'CO (a reducing gas) reacts with adsorbed oxygen on the tin oxide surface of the sensor, releasing electrons and reducing the electrical resistance of the sensor. Lower resistance means a larger share of the supply voltage falls across the fixed load resistor. The ADC reads this higher voltage as a higher digital number.',
                    'marks': 5,
                },
                {
                    'q': 'Today\'s MQ-7 ADC reading is 350. Calculate (a) the ADC voltage (350/4095 × 3.3V), (b) the sensor voltage (× 2 for divider), (c) the sensor resistance RS = 1000 × (5/Vsensor − 1).',
                    'answer_guide': '(a) 350/4095 × 3.3 = 0.282V. (b) 0.282 × 2 = 0.564V. (c) RS = 1000 × (5/0.564 − 1) = 1000 × 7.87 = 7,870 Ω. Accept ±5% for rounding.',
                    'marks': 6,
                },
            ],
            'vocabulary': [
                {'term': 'Incomplete Combustion', 'definition': 'Combustion with insufficient oxygen, producing carbon monoxide (CO) and/or soot rather than only CO₂ and water.'},
                {'term': 'Metal Oxide Semiconductor Sensor', 'definition': 'A gas sensor using a metal oxide (typically SnO₂) whose electrical resistance changes when target gases are present.'},
                {'term': 'Adsorption', 'definition': 'The adhesion of molecules from a gas or liquid onto a solid surface (distinct from absorption, which is bulk uptake).'},
                {'term': 'Voltage Divider', 'definition': 'A circuit of two resistors in series that produces an output voltage proportional to but smaller than the input voltage.'},
            ],
            'extension': (
                'Research the electrochemical CO sensor used in professional CO alarms. Compare '
                'its operating principle to the MQ-7 metal oxide sensor. List advantages and '
                'disadvantages of each type. Which would be more appropriate for a medical-grade '
                'air quality monitor, and why?'
            ),
            'curriculum_link': 'Nepal CDC Grade 9 Chemistry, Unit 3: Chemical Reactions; Grade 10 Physics, Unit 4: Electrical Circuits',
            'sdg_links': ['SDG 3: Good Health and Well-Being', 'SDG 7: Clean Energy', 'SDG 4: Quality Education'],
            'cross_curricular': [
                'Physics: Electrical resistance, voltage dividers, Ohm\'s law',
                'Mathematics: Algebra, formula application, unit conversion',
                'Health: CO poisoning, combustion and indoor air quality',
            ],
        },

        {
            'id': 'air-04',
            'title': 'Who Breathes Dirty Air?',
            'subtitle': 'Environmental justice, gender, poverty and the politics of clean air in Nepal',
            'grade_band': '11–12',
            'subjects': ['Sociology', 'Economics', 'Ethics', 'Health'],
            'duration': '60 min',
            'type': 'discussion',
            'overview': (
                'Students examine the unequal distribution of air pollution exposure across '
                'gender, class and geographic lines in Nepal, analyse the policy responses, '
                'and engage with the ethical frameworks of environmental justice.'
            ),
            'nepal_context': (
                'In Nepal, air pollution is not experienced equally. Women who cook with biomass '
                'fires are exposed to CO and PM2.5 for 3–6 hours per day. Children playing near '
                'cooking fires absorb disproportionate pollution relative to their body size. '
                'Urban poor communities live near heavily trafficked roads and brick kilns. '
                'Farmers who burn crop residue in spring often have no practical alternative. '
                'Wealthier households have switched to LPG or electric induction cookers and '
                'drive in sealed, air-conditioned vehicles. The capacity to avoid pollution '
                'closely tracks income, gender and geography. Clean air is, in practice, '
                'a luxury good in Nepal.'
            ),
            'learning_objectives': [
                'Define environmental justice and apply it to Nepal\'s air quality context.',
                'Analyse how gender, income and geography determine air pollution exposure in Nepal.',
                'Evaluate current Nepali government policies on air quality and cooking fuel transition.',
                'Construct an evidence-based policy recommendation for reducing inequitable air pollution exposure.',
            ],
            'background': (
                'Environmental justice is the principle that no community should bear a '
                'disproportionate share of environmental harms regardless of race, income, '
                'gender or other characteristics. It emerged from the US environmental justice '
                'movement in the 1980s but applies globally. In Nepal\'s context, the principle '
                'highlights how the same society can simultaneously include those with almost no '
                'pollution exposure (wealthy urban households with electric appliances) and those '
                'with extreme daily exposure (rural women cooking on open fires in unventilated '
                'kitchens).\n\n'
                'Nepal\'s government has implemented several relevant policies. The Subsidy on '
                'LPG policy has reduced (and complicated) fuel costs. The Biogas Support '
                'Programme (BSP-Nepal) has installed over half a million household biogas plants '
                'since 1992, displacing significant biomass burning. The Improved Cookstoves '
                'Programme attempts to reduce wood consumption and indoor smoke. The National '
                'Ambient Air Quality Standards set limits for outdoor pollutants, but enforcement '
                'is limited by monitoring capacity and political will.\n\n'
                'The gendered dimension deserves particular attention. The Global Burden of '
                'Disease study estimates that household air pollution is responsible for 6.7% '
                'of Nepal\'s total disease burden — and this burden falls disproportionately on '
                'women because traditional gender roles place women in the kitchen. A policy '
                'that reduces cooking smoke is therefore also a gender equity intervention, '
                'and this framing has been used successfully to access climate and health '
                'funding for clean cooking programmes in Nepal.'
            ),
            'teacher_notes': (
                'This activity is most powerful when students engage personally. Ask those from '
                'different backgrounds — urban and rural, different income levels — to share '
                'what fuel their family uses for cooking and whether they have experienced '
                'smoky kitchens. Make space for this without creating shame. The goal is to '
                'see the structural pattern in individual experiences, not to judge individual '
                'choices that are often not free choices at all.'
            ),
            'live_sensors': ['mq7_raw', 'mq135_raw'],
            'materials': ['Writing materials', 'Access to any Nepal policy document on clean cooking (optional)'],
            'procedure': [
                'Read the current air quality values. Note the time and any nearby pollution sources.',
                'Define "environmental justice" in your own words, then refine it after reading the background section.',
                'Create a table: three columns (Low-income rural woman / Middle-income urban man / Wealthy urban household), three rows (Pollution source they face / Hours of exposure per day / Capacity to reduce exposure). Fill it in for Nepal.',
                'Research: Nepal\'s Biogas Support Programme has installed 500,000+ household biogas units. Calculate what fraction of Nepal\'s approximately 5 million households this represents. Is this adequate?',
                'In pairs, design a policy intervention to reduce indoor air pollution in rural Nepal that explicitly addresses gender equity. Consider: who benefits, who pays, who decides, what barriers exist.',
                'Write a 250-word policy brief arguing for one specific government action on Nepal\'s clean cooking transition.',
            ],
            'discussion_questions': [
                'A woman who cooks with wood fire in rural Nepal does not "choose" to breathe polluted air in any meaningful sense. What structural factors constrain her choices? Who is responsible for changing them?',
                'The government subsidises LPG for cooking but the subsidy is often captured by urban households, not rural ones. What does this suggest about how policy design can reproduce inequality?',
                'Is air pollution in Nepal a health problem, an environmental problem, a gender problem, an economic problem, or all of these at once? What difference does the framing make to the solutions that are considered?',
            ],
            'worksheet_questions': [
                {
                    'q': 'Define "environmental justice" and explain with ONE specific example how it applies to air quality in Nepal.',
                    'answer_guide': 'Environmental justice means no community should bear a disproportionate share of environmental harm. Nepal example: rural women cooking on open fires bear extreme daily PM2.5 and CO exposure while wealthy urban households face minimal exposure — same country, radically different exposure based on income and gender.',
                    'marks': 4,
                },
                {
                    'q': 'Identify TWO ways that Nepal\'s clean cooking policies have been effective and TWO ways they have fallen short.',
                    'answer_guide': 'Effective: BSP-Nepal 500,000+ biogas units; LPG access has expanded in urban areas; cookstove programmes have reduced smoke in some areas. Fallen short: rural poor still largely excluded; LPG subsidies often captured by urban users; maintenance of improved stoves is poor; coverage remains partial. Award marks for specificity.',
                    'marks': 6,
                },
                {
                    'q': 'Why is reducing indoor air pollution from cooking fires simultaneously a health intervention AND a gender equity intervention? Explain the connection.',
                    'answer_guide': 'Because women bear the majority of cooking responsibilities in Nepal, they bear the majority of indoor air pollution exposure. Reducing cooking smoke therefore directly improves women\'s health outcomes disproportionately. It also frees women\'s time (gathering firewood, tending slow fires) and reduces chronic respiratory disease that disproportionately affects them.',
                    'marks': 4,
                },
            ],
            'vocabulary': [
                {'term': 'Environmental Justice', 'definition': 'The fair treatment and meaningful involvement of all people in environmental decision-making, regardless of race, income or gender.'},
                {'term': 'Disease Burden', 'definition': 'The total impact of a health problem on a population, measured as deaths, disability-adjusted life years (DALYs) or economic cost.'},
                {'term': 'Policy Capture', 'definition': 'When a policy intended to benefit a target population is diverted to benefit more powerful groups instead.'},
                {'term': 'Gendered Risk', 'definition': 'A risk that falls disproportionately on one gender due to social roles, biological differences or power inequalities.'},
            ],
            'extension': (
                'Find and read Nepal\'s National Ambient Air Quality Standards document. Compare '
                'the limits set for CO, PM2.5 and PM10 to WHO guidelines. For each pollutant, '
                'note whether Nepal\'s standard is stricter, weaker or equivalent to WHO. Write '
                'a paragraph evaluating whether Nepal\'s standards adequately protect health.'
            ),
            'curriculum_link': 'Nepal CDC Grade 11 Sociology, Unit 5: Social Inequality; Grade 12 Health Education, Unit 4: Environmental Health Policy',
            'sdg_links': ['SDG 3: Good Health', 'SDG 5: Gender Equality', 'SDG 10: Reduced Inequalities', 'SDG 7: Clean Energy'],
            'cross_curricular': [
                'Sociology: Gender roles, social inequality, environmental justice',
                'Economics: Cost of disease burden, subsidy policy, market failures',
                'English: Policy brief writing, persuasive argument',
                'Health: Epidemiology, burden of disease, gender and health',
            ],
        },

        {
            'id': 'air-05',
            'title': 'Environmental Health Research Methods',
            'subtitle': 'Designing an exposure assessment study — from sensor data to epidemiological evidence',
            'grade_band': 'UG',
            'subjects': ['Public Health', 'Environmental Science', 'Research Methods'],
            'duration': '90 min',
            'type': 'research',
            'overview': (
                'Undergraduate students design a rigorous exposure assessment study using the '
                'sensor hub, grapple with the gap between sensor readings and health-relevant '
                'concentrations, and write a study protocol suitable for ethical review.'
            ),
            'nepal_context': (
                'Nepal has a significant gap in environmental health data. Most published studies '
                'on air pollution in Nepal focus on Kathmandu; rural exposure data is almost '
                'absent from the peer-reviewed literature. This gap limits the evidence base '
                'for policy and perpetuates rural health inequities. Sensor networks like this '
                'one, properly documented and deployed, represent an opportunity to begin '
                'filling that gap — but only if the studies using them are designed to produce '
                'credible, publishable evidence.'
            ),
            'learning_objectives': [
                'Design a personal exposure assessment study using wearable or fixed sensors.',
                'Apply WHO air quality guidelines to interpret sensor readings in a health context.',
                'Identify and mitigate the main sources of bias and confounding in an air quality study.',
                'Write a study protocol including background, objectives, methods, analysis plan and ethics.',
            ],
            'background': (
                'Epidemiological studies of air pollution use one of two exposure assessment '
                'approaches: ambient monitoring (measuring pollution in the outdoor environment, '
                'typically at fixed stations) and personal exposure monitoring (measuring what '
                'an individual actually inhales over a 24-hour period). Personal exposure is '
                'always different from ambient because people move through different environments '
                '— home, kitchen, road, office — each with different pollution levels, and they '
                'breathe at different rates during different activities.\n\n'
                'The WHO 2021 Global Air Quality Guidelines set the following 24-hour mean limits: '
                'PM2.5 15 µg/m³; PM10 45 µg/m³; CO 4 mg/m³ (approximately 3.5 ppm); NO₂ 25 µg/m³. '
                'Our MQ sensors do not directly measure these concentrations — they produce '
                'relative resistance changes that can be converted to approximate ppm values '
                'only after careful calibration against certified gas standards. This is a '
                'critical limitation that must appear in any study protocol using this device.\n\n'
                'Confounding is the central methodological challenge in environmental health '
                'research. People who live near roads (high pollution exposure) are also more '
                'likely to be poor, to smoke, to have less access to healthcare and to work '
                'in physically demanding jobs. Attributing health differences to air pollution '
                'alone requires controlling for these other factors — through study design '
                '(matching, restriction) or statistical analysis (regression).'
            ),
            'teacher_notes': (
                'The study protocol produced in this activity should be evaluated using research '
                'methods criteria, not just content knowledge. Grade students on: clarity of '
                'research question, appropriateness of methods for the question, awareness of '
                'limitations, completeness of ethics considerations, and quality of writing. '
                'Encourage students to be honest about what this sensor can and cannot measure '
                '— acknowledging limitations is a mark of scientific maturity, not weakness.'
            ),
            'live_sensors': ['mq7_raw', 'mq135_raw'],
            'materials': ['WHO Air Quality Guidelines (2021)', 'Epidemiology textbook or reference', 'Word processor'],
            'procedure': [
                'Read today\'s MQ-7 and MQ-135 values plus their calculated sensor voltages. Calculate approximate relative CO level as a fraction of the sensor\'s typical maximum response.',
                'Identify the key gap: this sensor measures resistance changes, not calibrated ppm concentrations. Write a 100-word "Sensor Limitations" section for a study protocol.',
                'Define a specific research question your study would answer — e.g. "Does CO exposure in rural kitchens using biomass fuel exceed WHO 24-hour guideline levels during cooking?" Make it specific, measurable and answerable.',
                'Design the study: what population, how many participants, what measurement frequency, how long, what comparison group, what confounders to measure alongside air quality.',
                'Write a consent and ethics section: what are participants\' risks? What data will be collected? Who has access? How will data be stored and anonymised?',
                'Write a complete 800-word study protocol with sections: Background, Research Question, Methods, Analysis Plan, Limitations, Ethics.',
            ],
            'discussion_questions': [
                'Your sensor reads a raw ADC value of 600 during cooking. Without calibration data, what can you legitimately claim about CO exposure? What cannot you claim?',
                'A community members asks: "Is the air in my kitchen safe?" How do you answer responsibly given the sensor\'s calibration limitations?',
                'If you found that kitchen CO levels exceeded WHO guidelines during cooking, what would be the appropriate pathway from sensor data to public health action?',
            ],
            'worksheet_questions': [
                {
                    'q': 'Write a 100-word "Sensor Limitations" section for a study protocol using this device. Include at least three specific limitations.',
                    'answer_guide': 'Should include: no calibration against certified gas standards; MQ sensors respond to multiple gases (cross-sensitivity); readings affected by temperature and humidity; no direct PM2.5 measurement; voltage divider correction required; sensor drift over time without recalibration. Award marks for specificity and scientific accuracy.',
                    'marks': 5,
                },
                {
                    'q': 'What is confounding? Give one example of a potential confounder in a study comparing air pollution exposure and respiratory health in Nepal.',
                    'answer_guide': 'Confounding occurs when a third variable is associated with both the exposure and the outcome, creating an apparent relationship that is not causal. Example: poverty is associated with both high pollution exposure (biomass cooking, proximity to roads) and poor respiratory health (poor nutrition, limited healthcare access) — failure to account for poverty would confound a study of pollution and respiratory disease.',
                    'marks': 4,
                },
            ],
            'vocabulary': [
                {'term': 'Exposure Assessment', 'definition': 'The process of estimating the concentration of a pollutant and the duration of contact experienced by study participants.'},
                {'term': 'Confounding', 'definition': 'A situation where an observed association between exposure and outcome is distorted by a third variable associated with both.'},
                {'term': 'Ambient Monitoring', 'definition': 'Measurement of outdoor air pollution at fixed stations, representing average community exposure rather than individual exposure.'},
                {'term': 'DALY', 'definition': 'Disability-Adjusted Life Year — a measure of disease burden combining years of life lost to premature death and years lived with disability.'},
            ],
            'extension': (
                'Read one peer-reviewed paper on indoor air pollution in South Asia or Nepal '
                '(search Google Scholar for "household air pollution Nepal"). Critically evaluate '
                'its exposure assessment methods: what sensors or methods did they use, how did '
                'they handle calibration, what confounders did they control for, and what '
                'limitations do they acknowledge?'
            ),
            'curriculum_link': 'Undergraduate Public Health / Environmental Science Research Methods; aligns with Nepal Health Research Council ethical guidelines',
            'sdg_links': ['SDG 3: Good Health', 'SDG 4: Quality Education', 'SDG 17: Partnerships for the Goals'],
            'cross_curricular': [
                'Statistics: Confounding, regression, study design',
                'Ethics: Research ethics, informed consent, community benefit',
                'English: Scientific protocol writing, academic register',
                'Health Policy: Pathway from evidence to intervention',
            ],
        },
    ],
}
