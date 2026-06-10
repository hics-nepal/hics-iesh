SOIL = {
    'id': 'soil',
    'title': 'Soil & Agriculture',
    'icon': '🌱',
    'color': '#d29922',
    'tagline': 'Understanding what lies beneath — soil temperature, moisture and the land that feeds Nepal',
    'description': (
        'Soil is not merely dirt — it is a living system that stores water, cycles nutrients, '
        'anchors plants and feeds the majority of Nepal\'s population. This module uses soil '
        'temperature and moisture readings to explore soil science, Nepal\'s agricultural '
        'heritage, the threat of soil degradation, and the future of farming in a changing climate.'
    ),
    'sensors': ['soil_temp', 'soil_moist'],
    'teaching_guide': (
        'These activities are particularly powerful when students have access to an actual '
        'soil sample — even a pot of garden soil brought to class. Ask students to touch the '
        'soil and estimate its moisture before looking at the sensor, then compare their '
        'physical estimate to the reading. This grounds the technology in sensory experience. '
        'For activities involving traditional knowledge, invite a local farmer or elder if '
        'possible — the contrast and connection between lived knowledge and sensor data is '
        'one of the richest discussions in the entire curriculum.'
    ),
    'activities': [

        {
            'id': 'soil-01',
            'title': 'Soil is Alive',
            'subtitle': 'Discovering what temperature and moisture mean for the living world underfoot',
            'grade_band': '6–8',
            'subjects': ['Science', 'Home Science'],
            'duration': '30 min',
            'type': 'observation',
            'viz_type': 'hz-gauges',
            'viz_config': {
                'title': 'What are the soil conditions at the station right now?',
                'gauges': [
                    {
                        'key': 'soil_moist', 'label': 'Soil Moisture', 'unit': '%',
                        'min': 0, 'max': 100,
                        'zones': [
                            {'label': 'Wilting', 'color': '#f85149', 'pct': 15},
                            {'label': 'Dry', 'color': '#d29922', 'pct': 20},
                            {'label': 'Good for crops', 'color': '#3fb950', 'pct': 40},
                            {'label': 'Waterlogged', 'color': '#58a6ff', 'pct': 25},
                        ],
                        'fact': 'Most crops in Nepal grow best at 40–70% soil moisture.',
                    },
                    {
                        'key': 'soil_temp', 'label': 'Soil Temperature', 'unit': '°C',
                        'min': 5, 'max': 35,
                        'zones': [
                            {'label': 'Too cold', 'color': '#58a6ff', 'pct': 30},
                            {'label': 'Growing zone', 'color': '#3fb950', 'pct': 50},
                            {'label': 'Too hot', 'color': '#f85149', 'pct': 20},
                        ],
                        'fact': 'Rice seeds need soil above 15°C to germinate.',
                    },
                ],
            },
            'overview': (
                'Students observe soil moisture and temperature readings, relate them to plant '
                'health and growth, and begin to understand soil as a living system rather than '
                'inert ground.'
            ),
            'nepal_context': (
                'Nepal\'s terraced hillside farms — khet for irrigated rice and bari for rainfed '
                'crops — are among the most visually distinctive and engineered landscapes on '
                'Earth. Built over centuries, these terraces slow water movement, prevent erosion '
                'and create microclimates that extend the growing season. Every farmer who tends '
                'these terraces reads soil condition by touch, smell and the look of the crop — '
                'skills passed down through generations. This activity adds a numerical language '
                'to that ancient literacy.'
            ),
            'learning_objectives': [
                'Define soil moisture and soil temperature as measurable properties of the soil.',
                'Explain why both measurements matter for plant growth.',
                'Describe what healthy soil moisture levels look and feel like.',
                'Connect Nepal\'s agricultural traditions to the science of soil health.',
            ],
            'background': (
                'Soil temperature controls the rate of nearly every biological and chemical '
                'process in the ground. Most crop seeds will not germinate below 10°C. Soil '
                'bacteria and fungi — which break down organic matter into nutrients that plants '
                'can absorb — are most active between 20°C and 35°C. In Nepal\'s hills, soil '
                'temperature at planting depth (about 5 cm) determines whether seeds planted in '
                'early spring will germinate or rot. A sudden cold snap after planting can be '
                'catastrophic.\n\n'
                'Soil moisture is the percentage of the soil\'s pore spaces that are filled with '
                'water rather than air. Our capacitive sensor measures this as an electrical '
                'property — wet soil conducts electricity differently to dry soil. Plants need '
                'moisture in the root zone to draw water and dissolved nutrients upward. Too '
                'little water (drought stress) causes wilting and stunted growth. Too much '
                '(waterlogging) drives air out of the soil, suffocating roots and promoting '
                'root rot. The ideal range depends on the crop and soil type.\n\n'
                'Soil is not just minerals and water — it is home to billions of organisms per '
                'gram: bacteria, fungi, earthworms, nematodes, insects. These creatures drive '
                'nutrient cycling, create the loose structure that lets roots penetrate, and '
                'produce the characteristic earthy smell (caused by a compound called geosmin '
                'produced by Streptomyces bacteria). When we measure soil temperature and '
                'moisture, we are measuring the conditions for this entire community of life.'
            ),
            'teacher_notes': (
                'If possible, bring two samples of soil to class — one dry, one well-watered. '
                'Students will immediately grasp the concept of moisture content by handling '
                'both. Compare them: colour (wet soil is darker), texture (dry soil is crumbly, '
                'wet soil cohesive), weight (wet soil is heavier). Connect to the sensor reading: '
                'can students order the two samples from what the sensor would read?'
            ),
            'live_sensors': ['soil_temp', 'soil_moist'],
            'materials': ['Soil sample (optional)', 'Notebook'],
            'procedure': [
                'Read the current soil temperature and soil moisture from the dashboard. Record them.',
                'Look at the soil moisture bar chart on the dashboard. What does the bar height tell you?',
                'Touch some soil if available. Does it feel consistent with the moisture reading? (Very dry = crumbly, falls apart; Moist = holds shape when squeezed; Wet = releases water when squeezed)',
                'If you have two soil samples at different moisture levels, predict which will show a higher sensor reading before testing.',
                'Draw a simple diagram of a plant in soil. Label: roots, soil moisture zone, soil temperature zone, sunlight.',
                'Discuss with a partner: what would happen to the plant if the soil moisture dropped to near 0% for a week?',
            ],
            'discussion_questions': [
                'Why might a gardener water their plants in the early morning rather than midday? (Hint: think about what happens to soil moisture on a hot, sunny day.)',
                'Farmers in Nepal traditionally plant rice only after the first monsoon rains. What soil conditions are they waiting for?',
                'What might cause the soil temperature reading to be higher in the afternoon than in the morning?',
            ],
            'worksheet_questions': [
                {
                    'q': 'Record today\'s readings: Soil Temperature = ___ °C   Soil Moisture = ___ %',
                    'answer_guide': 'Observational — verify students read correct sensor values.',
                    'marks': 2,
                },
                {
                    'q': 'Give TWO reasons why soil temperature matters for growing crops.',
                    'answer_guide': 'Seeds need warmth to germinate (typically >10°C for most crops); soil bacteria and fungi that supply nutrients to plants are most active at 20–35°C; cold soil can cause roots to grow slowly or seeds to rot.',
                    'marks': 4,
                },
                {
                    'q': 'A farmer\'s soil moisture sensor shows 8%. Is this good for growing vegetables? Explain what the farmer should do.',
                    'answer_guide': '8% is very dry — below the wilting point for most vegetables. The farmer should irrigate. Most vegetables need 40–60% soil moisture. Students should also mention that watering should be gradual to avoid waterlogging.',
                    'marks': 3,
                },
            ],
            'vocabulary': [
                {'term': 'Soil Moisture', 'definition': 'The amount of water held in the spaces between soil particles, expressed as a percentage.'},
                {'term': 'Soil Temperature', 'definition': 'The temperature of the soil at a given depth, measured in degrees Celsius.'},
                {'term': 'Germination', 'definition': 'The process by which a seed begins to sprout and grow, requiring sufficient moisture, warmth and sometimes light.'},
                {'term': 'Nutrient Cycling', 'definition': 'The process by which soil organisms break down organic matter and release mineral nutrients that plants can absorb.'},
            ],
            'extension': (
                'Set up a simple experiment: plant identical seeds in two small pots with the '
                'same soil. Water one regularly and keep the other dry. Observe for two weeks '
                'and record the soil moisture using the sensor at each observation. Write a '
                'report on how moisture affected germination and growth.'
            ),
            'curriculum_link': 'Nepal CDC Grade 7 Compulsory Science, Unit 5: Plants and Soil; Grade 7 Home Science, Unit 3: Kitchen Gardening',
            'sdg_links': ['SDG 2: Zero Hunger', 'SDG 15: Life on Land'],
            'cross_curricular': [
                'Home Science: Kitchen gardening, growing vegetables',
                'Geography: Soil types across Nepal\'s regions',
                'Science: Plant biology, nutrient cycles',
            ],
        },

        {
            'id': 'soil-02',
            'title': 'Water in the Ground',
            'subtitle': 'Tracing the water cycle through soil — evaporation, infiltration and the monsoon\'s legacy',
            'grade_band': '8–10',
            'subjects': ['Science', 'Mathematics', 'Geography'],
            'duration': '45 min',
            'type': 'experiment',
            'overview': (
                'Students track how soil moisture changes over time, connect the readings to '
                'the water cycle, and calculate evaporation rates — building a quantitative '
                'understanding of how water moves through Nepal\'s landscapes.'
            ),
            'nepal_context': (
                'Nepal\'s hill and mountain regions are defined by their relationship with water. '
                'During the monsoon, 80% of annual rainfall arrives in four months; in the dry '
                'season, irrigation depends on water stored in soil, glaciers and aquifers. '
                'Terraced agriculture works partly because terraces slow water movement '
                'horizontally, giving it time to infiltrate vertically into the soil rather than '
                'running off and causing erosion. Understanding soil water storage is not '
                'abstract physics — it is the difference between a productive hillside farm '
                'and a bare, eroded slope.'
            ),
            'learning_objectives': [
                'Describe infiltration, evaporation and transpiration as components of the water cycle.',
                'Record soil moisture at regular intervals and construct a time-series graph.',
                'Calculate the rate of moisture change and interpret what drives it.',
                'Explain the link between soil water storage, irrigation and Nepal\'s terraced landscape.',
            ],
            'background': (
                'When rain falls on soil, water can take three paths: it can run off the surface '
                '(runoff), be absorbed into the soil (infiltration), or be intercepted by plant '
                'leaves and evaporate directly. Infiltrated water is stored in the tiny spaces '
                '(pores) between soil particles. From there it can be absorbed by plant roots '
                '(transpiration), evaporate from the soil surface, or drain downward to '
                'groundwater (percolation). Together, evaporation and transpiration are called '
                'evapotranspiration — the combined return of water from land to atmosphere.\n\n'
                'Soil texture determines how much water it can hold. Clay soils have tiny pores '
                'that hold water tightly but drain slowly. Sandy soils drain quickly but hold '
                'little water. Loam — a mixture of sand, silt and clay — is ideal for most crops '
                'as it holds adequate moisture while still draining freely. Much of Nepal\'s '
                'productive hill soil is loam enriched by centuries of organic matter from '
                'composted crop waste and animal manure.\n\n'
                'The rate at which soil loses moisture tells us about energy in the environment. '
                'On a hot, sunny day with low humidity, evapotranspiration is high and soil dries '
                'quickly. On a cool, cloudy, humid day — or after a monsoon rain — the soil '
                'stays wet for much longer. This is why monsoon-era soils remain productive '
                'for weeks after the rains stop: the soil acts as a reservoir.'
            ),
            'teacher_notes': (
                'The most powerful version of this activity records soil moisture readings at the '
                'start of class, at lunch and at the end of the day — or over multiple days. '
                'If the sensor is in outdoor soil, students can observe real drying curves and '
                'relate them to temperature and sunshine. Even if readings only span one lesson, '
                'extrapolating the rate of change to ask "when would the soil reach wilting '
                'point?" is a valuable exercise.'
            ),
            'live_sensors': ['soil_temp', 'soil_moist'],
            'materials': ['Graph paper', 'Calculator', 'Clock or timer'],
            'procedure': [
                'Record soil moisture now: ___ %. Record the time: ___',
                'Calculate: at what soil moisture level does the soil label change from "Moist" to "Dry" on the dashboard? (Read the threshold from the display.)',
                'Record moisture readings every 10 minutes for 30 minutes (3 readings total). Record temperature each time too.',
                'Plot your three moisture readings on a line graph (time on x-axis, moisture % on y-axis).',
                'Calculate the rate of moisture change: (final reading − first reading) ÷ (time in hours) = ___ %/hour.',
                'Predict: if this rate continued, when would the soil reach 20% moisture? Show your calculation.',
                'Discuss: what factors in the room or outside are causing the moisture to change? How would the rate differ on a rainy day versus a hot dry day?',
            ],
            'discussion_questions': [
                'After heavy monsoon rain, a field might reach 90% soil moisture. Using your measured rate of change, estimate how many days it would take to dry to 40%. What assumptions does this estimate require?',
                'Why do terraced rice paddies need to maintain very high soil moisture (near saturation) during the growing season?',
                'What would happen to Nepal\'s hillside farms if the monsoon arrived two months late?',
            ],
            'worksheet_questions': [
                {
                    'q': 'Record your three moisture readings with times. Calculate the rate of change in %/hour. Show your working.',
                    'answer_guide': 'Check arithmetic. Rate = (reading 3 − reading 1) ÷ (time elapsed in hours). Negative rate means drying; positive means wetting.',
                    'marks': 5,
                },
                {
                    'q': 'Explain what "infiltration" means and describe what type of soil (clay, sand or loam) would have the highest infiltration rate.',
                    'answer_guide': 'Infiltration is the process of water moving from the surface into the soil. Sandy soil has the highest infiltration rate because its large particles create large pores. Clay has the lowest rate; loam is intermediate.',
                    'marks': 4,
                },
                {
                    'q': 'A farmer notices the soil moisture sensor drops from 60% to 25% in one day during a hot, sunny period in May. What does this suggest about evapotranspiration rates? What should the farmer do?',
                    'answer_guide': 'High evapotranspiration due to hot weather, direct sunlight, and possibly low humidity. The farmer should irrigate to bring moisture back above the wilting threshold (approximately 30–40% for most crops). Mulching would help reduce further evaporation.',
                    'marks': 4,
                },
            ],
            'vocabulary': [
                {'term': 'Infiltration', 'definition': 'The movement of water from the soil surface downward into the soil profile.'},
                {'term': 'Evapotranspiration', 'definition': 'The combined loss of water from soil evaporation and plant transpiration to the atmosphere.'},
                {'term': 'Field Capacity', 'definition': 'The soil moisture level after excess water has drained away — typically the upper limit of useful moisture for plants.'},
                {'term': 'Wilting Point', 'definition': 'The minimum soil moisture below which plants can no longer extract water and begin to wilt permanently.'},
            ],
            'extension': (
                'Research the Penman-Monteith equation — the standard method used by agronomists '
                'worldwide to estimate evapotranspiration from temperature, humidity and wind speed. '
                'Which of these variables can our sensor hub measure? What additional sensors '
                'would be needed for a complete FAO-standard calculation?'
            ),
            'curriculum_link': 'Nepal CDC Grade 8 Compulsory Science, Unit 6: Water and Its Uses; Grade 9 Geography, Unit 3: Water Resources of Nepal',
            'sdg_links': ['SDG 2: Zero Hunger', 'SDG 6: Clean Water and Sanitation', 'SDG 15: Life on Land'],
            'cross_curricular': [
                'Mathematics: Rate of change, extrapolation, line graphs',
                'Geography: Water cycle, Nepal\'s irrigation systems, terrace agriculture',
                'Physics: Evaporation as energy transfer',
            ],
        },

        {
            'id': 'soil-03',
            'title': 'Farming with Data',
            'subtitle': 'How sensor readings can support better agricultural decisions — and what that means for Nepal',
            'grade_band': '9–10',
            'subjects': ['Agriculture', 'Economics', 'ICT'],
            'duration': '45 min',
            'type': 'analysis',
            'overview': (
                'Students use soil data to simulate agricultural decision-making, explore the '
                'concept of precision agriculture, and assess whether data-driven farming is '
                'accessible and appropriate for Nepal\'s smallholder context.'
            ),
            'nepal_context': (
                'Over 60% of Nepal\'s workforce is in agriculture, mostly on small plots of less '
                'than 0.5 hectares. These farmers are highly skilled but often lack access to '
                'the kind of quantitative feedback that can prevent over-irrigation (wasting '
                'water and labour), under-irrigation (losing crops) or planting into cold soil '
                '(losing seeds). Nepal\'s government and several NGOs are piloting low-cost '
                'sensor networks for smallholder farmers, but questions of cost, training, '
                'connectivity and cultural fit remain real barriers.'
            ),
            'learning_objectives': [
                'Interpret soil sensor readings to make an irrigation scheduling recommendation.',
                'Define precision agriculture and evaluate its potential benefits and limitations.',
                'Analyse the economic argument for sensor-based farming on a smallholder scale.',
                'Assess barriers to technology adoption in rural Nepal and propose realistic solutions.',
            ],
            'background': (
                'Precision agriculture uses sensors, GPS and data analysis to manage crops at '
                'fine spatial and temporal scales — adjusting irrigation, fertiliser and pesticide '
                'applications exactly where and when they are needed, rather than applying uniform '
                'treatments to entire fields. Originally developed for large-scale mechanised farms '
                'in the USA and Australia, it is now being adapted for smallholder contexts in '
                'South and Southeast Asia.\n\n'
                'The core economic argument is simple: over-irrigation wastes water and the labour '
                'to apply it; under-irrigation reduces yield. A sensor that tells you precisely '
                'when and how much to water can increase water-use efficiency by 20–40% while '
                'maintaining or improving yields. In a country like Nepal where water is seasonally '
                'scarce and irrigation infrastructure is expensive to build, these efficiency gains '
                'have direct economic value.\n\n'
                'However, technology adoption in farming is not just about the technology. It requires '
                'that farmers trust the new tool, can afford it, can maintain it, and can interpret '
                'its outputs in the context of their own deep knowledge of their land and crops. '
                'A sensor that shows "35% moisture" means nothing to a farmer who has never used '
                'the concept of percentage moisture — but the same information can be presented as '
                'a visual bar that maps directly to what the farmer already knows about soil feel.'
            ),
            'teacher_notes': (
                'This activity intentionally includes a critical perspective on technology adoption '
                '— do not let the lesson become simply a celebration of "tech solves farming." '
                'The most valuable discussions emerge when students grapple with who benefits, '
                'who bears the costs, and what existing farmer knowledge is displaced or devalued '
                'when external technology arrives. The comparison between sensor output and '
                'farmer intuition is not a test of which is better — both are valuable and '
                'complementary.'
            ),
            'live_sensors': ['soil_temp', 'soil_moist'],
            'materials': ['Calculator', 'Crop water requirement table (provided below)', 'Writing materials'],
            'procedure': [
                'Read current soil moisture: ___ %. Read current soil temperature: ___ °C.',
                'Use the decision table: if soil moisture < 30%: irrigate immediately; if 30–50%: irrigate within 24 hours; if 50–70%: monitor; if > 70%: no irrigation needed.',
                'Based on the current reading, what irrigation action would you recommend? Justify this with reference to the sensor value.',
                'Scenario: a farmer has 1,000 litres of water available. Their 200 m² plot needs to go from 25% to 55% moisture. Each 10% increase requires approximately 20 litres per m². Calculate whether the farmer has enough water for one full application.',
                'Group discussion: a low-cost soil moisture sensor costs approximately NPR 3,000. If it saves one unnecessary irrigation (estimated cost: NPR 800 in water and labour) per month, how many months to break even? What other factors would you consider?',
                'Write a 150-word recommendation to a rural farming cooperative explaining in plain language whether they should invest in soil sensors for their shared fields.',
            ],
            'discussion_questions': [
                'What might a farmer who has farmed the same land for 30 years know about their soil that no sensor can measure?',
                'Is precision agriculture appropriate for all types of Nepali farming? What types of farms or crops would benefit most?',
                'What would need to change in Nepal\'s agricultural system to make sensor-based farming accessible to farmers who cannot read or do not have smartphones?',
            ],
            'worksheet_questions': [
                {
                    'q': 'Based on today\'s soil moisture reading, state your irrigation recommendation and justify it in two sentences.',
                    'answer_guide': 'Accept any recommendation consistent with the decision table and the actual reading. Justification should reference the specific moisture value and the threshold.',
                    'marks': 3,
                },
                {
                    'q': 'Calculate whether 1,000 litres is sufficient to raise a 200 m² plot from 25% to 55% moisture. Show your working.',
                    'answer_guide': '30% increase needed. 20 litres per m² per 10% = 60 litres per m² total. 200 m² × 60 litres/m² = 12,000 litres required. 1,000 litres is NOT sufficient — covers only about 8% of the area. Full marks for correct calculation and correct conclusion.',
                    'marks': 5,
                },
                {
                    'q': 'Identify TWO barriers to sensor adoption for smallholder farmers in remote hill districts of Nepal. For each barrier, suggest a realistic solution.',
                    'answer_guide': 'Barriers: cost; lack of connectivity; literacy/training; power supply; language; cultural trust; lack of maintenance support. Solutions should be realistic given Nepal\'s context — e.g. cooperative ownership, visual displays, solar power, local language interfaces, farmer training programs.',
                    'marks': 6,
                },
            ],
            'vocabulary': [
                {'term': 'Precision Agriculture', 'definition': 'The use of sensors, data and technology to manage crops at fine scales, applying inputs only where and when they are needed.'},
                {'term': 'Irrigation Scheduling', 'definition': 'Deciding when and how much to water based on crop needs and soil moisture conditions.'},
                {'term': 'Water-Use Efficiency', 'definition': 'The amount of crop produced per unit of water used — higher efficiency means less water is wasted.'},
                {'term': 'Technology Adoption', 'definition': 'The process by which a community integrates a new tool or method into its practice, involving trust, training, cost and cultural fit.'},
            ],
            'extension': (
                'Research one real Nepali NGO or government programme working on smart agriculture '
                'or sensor-based farming. Write a one-page evaluation: what are they doing, '
                'who benefits, what are the limitations of their approach, and what would you '
                'recommend they change?'
            ),
            'curriculum_link': 'Nepal CDC Grade 9 Compulsory Science, Unit 7: Agriculture and Technology; Grade 10 Economics, Unit 4: Agriculture and Development',
            'sdg_links': ['SDG 2: Zero Hunger', 'SDG 8: Decent Work and Economic Growth', 'SDG 12: Responsible Consumption'],
            'cross_curricular': [
                'Economics: Cost-benefit analysis, break-even calculation',
                'ICT: Sensors, data-driven decision making, appropriate technology',
                'Social Studies: Rural livelihoods, smallholder farming, technology and society',
            ],
        },

        {
            'id': 'soil-04',
            'title': 'Traditional Wisdom and Modern Sensors',
            'subtitle': 'Two ways of knowing the land — and why Nepal needs both',
            'grade_band': '10–11',
            'subjects': ['Social Studies', 'Science', 'English', 'Philosophy'],
            'duration': '60 min',
            'type': 'discussion',
            'overview': (
                'Students compare traditional ecological knowledge from Nepali farming communities '
                'with sensor-based measurements, examining what each can and cannot reveal, '
                'and practise writing a structured comparative argument.'
            ),
            'nepal_context': (
                'Nepali farmers — particularly in indigenous communities like the Tharu in the '
                'Terai, Gurung in the hills, and Sherpa in the mountains — carry centuries of '
                'accumulated ecological knowledge about soil, water and climate. Tharu farmers '
                'traditionally assess soil readiness for planting by its colour, smell, texture '
                'and the behaviour of earthworms. Gurung herders know which grasses appear when '
                'soil moisture crosses certain thresholds. This is not superstition — it is '
                'careful empirical observation accumulated across generations. Development '
                'organisations and scientists are increasingly recognising this knowledge as '
                'complementary to, not competing with, sensor data.'
            ),
            'learning_objectives': [
                'Define "traditional ecological knowledge" (TEK) and explain its epistemological basis.',
                'Compare the strengths and limitations of TEK and sensor-based measurement.',
                'Construct a written comparative argument using evidence from both sources of knowledge.',
                'Reflect critically on how technology can marginalise existing knowledge systems.',
            ],
            'background': (
                'Epistemology is the branch of philosophy that asks: how do we know what we know? '
                'Western scientific knowledge is built on reproducible measurement, peer review '
                'and mathematical models. Traditional ecological knowledge (TEK) is built on '
                'direct observation, intergenerational transmission, embodied experience and '
                'spiritual or cultural frameworks. Both are empirical — based on evidence — but '
                'they collect, interpret and transmit that evidence differently.\n\n'
                'TEK has genuine scientific value. Indigenous land managers in Nepal often know '
                'microclimatic variations — shaded slopes that hold moisture longer, fields that '
                'drain poorly after rain, frost pockets in mountain valleys — that would take '
                'decades of sensor data to document. Their knowledge is site-specific, long-term '
                'and calibrated to the crops and conditions they manage. It also integrates '
                'multiple variables simultaneously: a Tharu farmer reading soil readiness for '
                'planting is simultaneously assessing temperature, texture, moisture, recent '
                'rainfall and the maturity of indicator plants.\n\n'
                'Sensor data offers different strengths: it is quantified (enabling comparison '
                'across sites and over time), it can be transmitted and shared remotely, it '
                'does not depend on any individual being present, and it can detect subtle '
                'changes that the human senses cannot reliably measure (a 0.5°C shift in soil '
                'temperature, a 3% change in moisture). The risk is that when sensor data '
                'arrives in a community, it can implicitly devalue existing knowledge — '
                'suggesting that what cannot be measured with instruments does not count.'
            ),
            'teacher_notes': (
                'If possible, invite a farmer or community elder to this session to speak about '
                'how they assess soil conditions. Ask them directly: what do they look for? '
                'When do they plant? How do they know when the soil is ready? Then compare '
                'their indicators to the sensor reading. This is not a test of who is right — '
                'the goal is to show that both are valid forms of knowledge with different '
                'strengths. The philosophical question of whether measurement displaces '
                'wisdom is genuinely difficult and worth leaving open.'
            ),
            'live_sensors': ['soil_temp', 'soil_moist'],
            'materials': ['Soil sample (optional)', 'Writing materials'],
            'procedure': [
                'Read the current soil temperature and moisture. Note them down.',
                'Before consulting the sensor, hold some soil in your hand (if available). How would you describe its moisture level? Its temperature? Its readiness for planting?',
                'Interview a partner: "If you were a farmer who had farmed this land for 20 years, what other signs would you look for to assess soil health — without any instruments?" List at least five indicators.',
                'For each indicator your partner named, discuss: Can a sensor measure this? Can the sensor measure something equivalent? Or is it measuring something different?',
                'Read the Nepal context above. Write a table with two columns: What TEK can tell us that sensors cannot / What sensors can tell us that TEK cannot. Aim for three entries in each column.',
                'Write a 200-word argument responding to: "Sensor data makes traditional ecological knowledge obsolete." Use evidence from the table to support your position.',
            ],
            'discussion_questions': [
                'If a sensor contradicts the intuition of an experienced farmer, who should be believed, and how should the disagreement be investigated?',
                'What is lost if younger generations rely entirely on sensors and stop learning traditional soil-reading skills?',
                'Can you think of any situation where traditional ecological knowledge would give you information a sensor simply cannot?',
            ],
            'worksheet_questions': [
                {
                    'q': 'Define "traditional ecological knowledge" and give ONE specific example from Nepal.',
                    'answer_guide': 'TEK is the accumulated knowledge, practices and beliefs of indigenous and local communities about the natural world, transmitted across generations. Nepal examples: Tharu soil readiness assessment by smell and texture; Sherpa glacier and weather reading by cloud patterns; Gurung indicator plant knowledge for soil moisture.',
                    'marks': 3,
                },
                {
                    'q': 'Write a table comparing THREE strengths and THREE limitations of sensor-based measurement versus traditional ecological knowledge.',
                    'answer_guide': 'Sensors: strengths include quantification, remote transmission, 24h monitoring, fine temporal resolution. Limitations: no cultural context, cost, power dependence, limited to measured variables. TEK: strengths include site-specificity, long time horizon, multivariate integration, no technology dependence. Limitations: not easily transferred across sites, may be lost with elders, hard to compare objectively.',
                    'marks': 6,
                },
                {
                    'q': 'Do you think Nepal\'s agricultural development programmes should actively work to document and preserve TEK alongside sensor networks? Argue your position in 100 words.',
                    'answer_guide': 'Accept well-reasoned arguments in either direction. Award marks for quality of reasoning, use of evidence and acknowledgement of counter-arguments.',
                    'marks': 5,
                },
            ],
            'vocabulary': [
                {'term': 'Traditional Ecological Knowledge (TEK)', 'definition': 'Accumulated knowledge about local ecosystems held by indigenous and local communities, transmitted orally across generations.'},
                {'term': 'Epistemology', 'definition': 'The branch of philosophy concerned with the nature, sources and limits of knowledge — how we know what we know.'},
                {'term': 'Indicator Species / Plant', 'definition': 'An organism whose presence, absence or behaviour signals something about environmental conditions.'},
                {'term': 'Complementary Knowledge', 'definition': 'Different knowledge systems that each reveal aspects the other cannot, and that together provide a more complete understanding.'},
            ],
            'extension': (
                'Conduct a structured interview with a farmer, gardener or elder in your community. '
                'Ask specifically about how they read soil conditions, when they plant, and how '
                'they know their soil is healthy. Write up your findings as a 400-word ethnographic '
                'note and compare at least two of their indicators to what our sensor measures.'
            ),
            'curriculum_link': 'Nepal CDC Grade 11 Social Studies, Unit 4: Indigenous Knowledge and Environment; Grade 10 English, Unit: Argumentative Writing',
            'sdg_links': ['SDG 2: Zero Hunger', 'SDG 15: Life on Land', 'SDG 11: Sustainable Communities'],
            'cross_curricular': [
                'Philosophy: Epistemology, ways of knowing',
                'English: Comparative argument writing',
                'Anthropology / Social Studies: Indigenous knowledge systems, Nepal\'s communities',
                'Science: Empirical method, observation-based knowledge',
            ],
        },

        {
            'id': 'soil-05',
            'title': 'Soil Health Assessment and Land Use',
            'subtitle': 'A multi-indicator assessment of soil condition and its implications for sustainable land management',
            'grade_band': 'UG',
            'subjects': ['Agronomy', 'Environmental Science', 'Development Studies'],
            'duration': '90 min',
            'type': 'research',
            'overview': (
                'Undergraduate students conduct a field-style soil health assessment using sensor '
                'data alongside physical and chemical indicators, evaluate land use history, and '
                'write a management recommendation report applicable to Nepal\'s agricultural context.'
            ),
            'nepal_context': (
                'Nepal loses an estimated 240 million tonnes of soil annually to erosion — one '
                'of the highest erosion rates in Asia. Steep topography, deforestation, monsoon '
                'intensity and agricultural intensification all contribute. In the hills, '
                'abandonment of traditional terrace maintenance as rural populations migrate '
                'to cities is accelerating erosion on previously stable slopes. Understanding '
                'soil health through multiple indicators — not just moisture and temperature — '
                'is essential for designing evidence-based land restoration programmes.'
            ),
            'learning_objectives': [
                'Apply a multi-indicator soil health framework integrating sensor data with physical and visual assessment.',
                'Interpret soil temperature and moisture patterns in the context of land use history and management.',
                'Write a professional soil health report with actionable management recommendations.',
                'Evaluate the adequacy of sensor-based assessment versus comprehensive soil analysis.',
            ],
            'background': (
                'Soil health is a broader concept than simple fertility. It encompasses the '
                'soil\'s capacity to function as a living system — cycling nutrients, filtering '
                'water, supporting biodiversity, and maintaining structure under management '
                'pressure. The USDA defines soil health as "the continued capacity of soil to '
                'function as a vital living ecosystem that sustains plants, animals and humans."\n\n'
                'A comprehensive soil health assessment typically measures: organic matter content, '
                'bulk density (compaction), aggregate stability, earthworm counts, pH, plant-available '
                'nutrients (N, P, K), electrical conductivity, and biological activity (measured '
                'as microbial biomass or respiration rate). Our sensor hub measures temperature '
                'and moisture — two important indicators but only two of many. Temperature and '
                'moisture interact strongly with biological activity: soil respiration (a proxy '
                'for microbial health) roughly doubles for every 10°C increase in temperature '
                '(the Q10 rule), and is maximised at around 60% water-filled pore space.\n\n'
                'Land use history is critical context for interpreting sensor readings. A '
                'recently ploughed field will show very different moisture dynamics from a '
                'long-term no-till plot. A slope that lost its topsoil to erosion will warm '
                'and dry faster than a deep-soil plot. Understanding what the numbers mean '
                'requires knowing the history of the land.'
            ),
            'teacher_notes': (
                'This activity works best if students can access or recall information about '
                'the land use history of the sensor\'s installation site: Is it irrigated? '
                'What crop was last grown? Is it on a slope? Was it recently tilled? This '
                'contextualises the readings in a way that connects to professional practice. '
                'The report-writing component should be assessed using the same criteria as '
                'a professional consultancy report: clarity, evidence, actionable recommendations, '
                'acknowledgement of limitations.'
            ),
            'live_sensors': ['soil_temp', 'soil_moist'],
            'materials': ['Spade or trowel for soil sampling (optional)', 'pH test kit (optional)', 'Reference: FAO Soil Health Indicators guidelines'],
            'procedure': [
                'Record soil temperature and moisture over a 30-minute period (5 readings). Calculate mean and standard deviation for each.',
                'Conduct a rapid visual assessment: soil colour, presence of earthworms, smell (earthy = active microbial community, rotten = anaerobic conditions), aggregate structure (does soil clump or fall apart?)',
                'Research the Q10 rule: given today\'s soil temperature, estimate relative microbial activity as a percentage of peak activity (which occurs at approximately 30°C).',
                'Using the formula: Water-Filled Pore Space (WFPS) % ≈ soil moisture % × 1.3 (for average Nepali hill soils), calculate WFPS and locate it on the optimal range for microbial activity (55–70% WFPS).',
                'Document land use history of the sensor site. Identify at least THREE factors in that history that would affect interpretation of the current readings.',
                'Write a 600-word soil health assessment report with sections: Site Description, Sensor Findings, Visual Assessment, Interpretation, Management Recommendations, and Limitations.',
            ],
            'discussion_questions': [
                'A soil has 75% moisture and 15°C temperature. Is this good or bad? What additional information do you need before you can answer?',
                'You are advising a reforestation programme on a degraded hillside in Sindhupalchok. What soil health data would you want beyond what this sensor can provide?',
                'How should sensor-based soil monitoring data be integrated with Nepal\'s national soil survey database? Who should own and have access to this data?',
            ],
            'worksheet_questions': [
                {
                    'q': 'Calculate mean and standard deviation for your five soil moisture readings. Interpret what the standard deviation tells you about moisture variability.',
                    'answer_guide': 'Check arithmetic. High standard deviation (>5%) suggests the soil is changing rapidly (drying or wetting event); low standard deviation suggests stable conditions. Students should interpret, not just calculate.',
                    'marks': 6,
                },
                {
                    'q': 'Apply the Q10 rule to estimate microbial activity at today\'s soil temperature relative to the optimal 30°C. Show your calculation.',
                    'answer_guide': 'Q10 ≈ 2 means activity doubles per 10°C increase. At 20°C: activity = 100% × 2^((20-30)/10) = 100% × 2^(-1) = 50% of peak. At 25°C: 70.7% of peak. Award marks for correct formula application.',
                    'marks': 5,
                },
            ],
            'vocabulary': [
                {'term': 'Soil Health', 'definition': 'The continued capacity of soil to function as a living ecosystem — cycling nutrients, supporting biodiversity and maintaining structure.'},
                {'term': 'Q10 Rule', 'definition': 'The observation that biological reaction rates approximately double for every 10°C increase in temperature.'},
                {'term': 'Water-Filled Pore Space (WFPS)', 'definition': 'The fraction of soil pores occupied by water rather than air — a key determinant of microbial activity and greenhouse gas emissions.'},
                {'term': 'Bulk Density', 'definition': 'The mass of dry soil per unit volume — a measure of compaction. High bulk density restricts root growth.'},
            ],
            'extension': (
                'Design a low-cost soil health monitoring kit for a Nepali hill farming cooperative '
                'that goes beyond temperature and moisture. What sensors would you add, what '
                'physical tests would complement them, and how would you present results to '
                'farmers without technical training? Prepare a one-page design proposal.'
            ),
            'curriculum_link': 'Undergraduate Agricultural Science / Environmental Science; aligns with FAO Voluntary Guidelines on Sustainable Soil Management',
            'sdg_links': ['SDG 2: Zero Hunger', 'SDG 15: Life on Land', 'SDG 13: Climate Action'],
            'cross_curricular': [
                'Statistics: Mean, standard deviation, interpretation of variability',
                'Biology: Microbial ecology, decomposition, nutrient cycling',
                'Development Studies: Land degradation, Nepal\'s agricultural policy',
                'Professional Writing: Consultancy report format',
            ],
        },
    ],
}
