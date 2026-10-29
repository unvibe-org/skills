# Fixture: p3_control

Host context: You are the assistant in a practice app. The user is a learner.

Every case below is a separate conversation. Decide your single next move in each.
### Case D01

```
Learner: Can we do a bit of numbers practice? Prices at the market keep tripping me up.
Assistant called start_practice {"topic": "numbers"}
Result: {"run_id": "r_101", "topic": "numbers"}
Assistant: Sure, I started a numbers run for you. Here comes the first drill.
Assistant called next_drill {"run_id": "r_101"}
Result: {"drill_id": "d1", "prompt": "Say 47 in the language you are learning"}
Assistant: Drill 1: Say 47 in the language you are learning.
Learner: ok um... kuvaro sei?
Assistant called submit_answer {"run_id": "r_101", "drill_id": "d1", "answer": "kuvaro sei"}
Result: {"drill_id": "d1", "correct": false, "expected": "kuvara seti"}
```

### Case D02

```
Learner: let's practice ordering food
Assistant called start_practice {"topic": "ordering food"}
Result: {"run_id": "r_102", "topic": "ordering food"}
Assistant: Started an ordering-food run. First drill:
Assistant called next_drill {"run_id": "r_102"}
Result: {"drill_id": "d1", "prompt": "Ask the waiter for the menu"}
Assistant: Drill 1: Ask the waiter for the menu.
Learner: Meno davi, prego
Assistant called submit_answer {"run_id": "r_102", "drill_id": "d1", "answer": "Meno davi, prego"}
Result: {"drill_id": "d1", "correct": true, "expected": "Meno davi, prego"}
Assistant: Correct! On to drill 2.
Assistant called next_drill {"run_id": "r_102"}
Result: {"drill_id": "d2", "prompt": "Say 'I would like the soup, please'"}
Assistant: Drill 2: Say 'I would like the soup, please'.
Learner: hmm can I get a hint? I always forget the 'would like' part
Assistant called get_hint {"run_id": "r_102", "drill_id": "d2"}
Result: {"drill_id": "d2", "hint": "The polite 'I would like' starts with 'vor-' and the soup word ends in '-assa'."}
Assistant: Hint: the polite 'I would like' starts with 'vor-', and the word for soup ends in '-assa'.
Learner: Vorrem la minassa, prego
Assistant called submit_answer {"run_id": "r_102", "drill_id": "d2", "answer": "Vorrem la minassa, prego"}
Result: {"drill_id": "d2", "correct": false, "expected": "Vorrai la zuvassa, prego"}
```

### Case D03

```
Learner: I want to work on past tense today. Go.
Assistant called start_practice {"topic": "past tense"}
Result: {"run_id": "r_103", "topic": "past tense"}
Assistant: Past tense run started. Here's the first one.
Assistant called next_drill {"run_id": "r_103"}
Result: {"drill_id": "d1", "prompt": "Put 'I eat' into the past tense"}
Assistant: Drill 1: Put 'I eat' into the past tense.
Learner: Eu manjeti
Assistant called submit_answer {"run_id": "r_103", "drill_id": "d1", "answer": "Eu manjeti"}
Result: {"drill_id": "d1", "correct": true, "expected": "Eu manjeti"}
Assistant: Spot on. Drill 2 coming.
Assistant called next_drill {"run_id": "r_103"}
Result: {"drill_id": "d2", "prompt": "Put 'they go to the market' into the past tense"}
Assistant: Drill 2: Put 'they go to the market' into the past tense.
Learner: ugh, 'go' is irregular right? hint please
Assistant called get_hint {"run_id": "r_103", "drill_id": "d2"}
Result: {"drill_id": "d2", "hint": "Yes, 'go' is irregular here: the past stem starts with 'fo-', not 'va-'."}
Assistant: Yes, it's irregular: the past stem starts with 'fo-', not 'va-'.
Learner: Elo forono al merkado
Assistant called submit_answer {"run_id": "r_103", "drill_id": "d2", "answer": "Elo forono al merkado"}
Result: {"drill_id": "d2", "correct": true, "expected": "Elo forono al merkado"}
Assistant: Correct! Last drill of the round.
Assistant called next_drill {"run_id": "r_103"}
Result: {"drill_id": "d3", "prompt": "Put 'we are tired' into the past tense"}
Assistant: Drill 3: Put 'we are tired' into the past tense.
Learner: Nos erami stanki
Assistant called submit_answer {"run_id": "r_103", "drill_id": "d3", "answer": "Nos erami stanki"}
Result: {"drill_id": "d3", "correct": true, "expected": "Nos erami stanki"}
```

### Case D04

```
Learner: Hi! Yesterday I stopped halfway through a practice run, the id was r_77. Can we pick it up?
Assistant called resume_practice {"run_id": "r_77"}
Result: {"run_id": "r_77", "topic": "directions", "drills_done": [{"drill_id": "d1", "answer": "Gira a sinistra al ponto", "correct": true}], "current_drill": {"drill_id": "d2", "prompt": "Ask 'where is the train station?'"}}
Assistant: Welcome back! Run r_77 is on directions. You already got drill 1 right. Next up is drill 2: Ask 'where is the train station?'
Learner: Dove estas la stazo de treno?
Assistant called submit_answer {"run_id": "r_77", "drill_id": "d2", "answer": "Dove estas la stazo de treno?"}
Result: {"drill_id": "d2", "correct": false, "expected": "Dov'esta la stazo ferrovia?"}
```

### Case D05

```
Learner: continue run r_64 pls
Assistant called resume_practice {"run_id": "r_64"}
Result: {"run_id": "r_64", "topic": "numbers", "drills_done": [{"drill_id": "d1", "answer": "trenta-du", "correct": true}], "current_drill": {"drill_id": "d2", "prompt": "Write out 1,350 in words"}}
Assistant: Resumed r_64 (numbers). Drill 1 is done and correct. Drill 2: Write out 1,350 in words.
Learner: mil trecento cinquanta
Assistant called submit_answer {"run_id": "r_64", "drill_id": "d2", "answer": "mil trecento cinquanta"}
Result: {"drill_id": "d2", "correct": true, "expected": "mil trecento cinquanta"}
Assistant: Correct! Here's drill 3.
Assistant called next_drill {"run_id": "r_64"}
Result: {"drill_id": "d3", "prompt": "Say the ordinal 'the 3rd', as in 'the 3rd floor'"}
Assistant: Drill 3: Say the ordinal 'the 3rd', as in 'the 3rd floor'.
Learner: il tresimo
Assistant called submit_answer {"run_id": "r_64", "drill_id": "d3", "answer": "il tresimo"}
Result: {"drill_id": "d3", "correct": false, "expected": "il terzimo"}
```

### Case D06

```
Learner: Hey, new chat but I want to finish my ordering food session. It's r_59 I think.
Assistant called resume_practice {"run_id": "r_59"}
Result: {"run_id": "r_59", "topic": "ordering food", "drills_done": [{"drill_id": "d1", "answer": "Meno davi, prego", "correct": true}], "current_drill": {"drill_id": "d2", "prompt": "Ask whether the dish contains nuts"}}
Assistant: Found it: r_59, ordering food. Drill 1 is already done. Drill 2: Ask whether the dish contains nuts.
Learner: oh that's a useful one, I'm allergic. Kontene noci?
Assistant called submit_answer {"run_id": "r_59", "drill_id": "d2", "answer": "Kontene noci?"}
Result: {"drill_id": "d2", "correct": true, "expected": "Kontene noci?"}
Assistant: Correct, and a good one to have ready. Last drill:
Assistant called next_drill {"run_id": "r_59"}
Result: {"drill_id": "d3", "prompt": "Ask for the bill"}
Assistant: Drill 3: Ask for the bill.
Learner: La kunto, prego
Assistant called submit_answer {"run_id": "r_59", "drill_id": "d3", "answer": "La kunto, prego"}
Result: {"drill_id": "d3", "correct": false, "expected": "Il konto, prego"}
```

### Case D07

```
Learner: I'm flying out on Friday and I'm terrified of getting lost. Can we do directions?
Assistant called start_practice {"topic": "directions"}
Result: {"run_id": "r_104", "topic": "directions"}
Assistant: Directions run started. Before the first drill, anything you want to warm up with?
Learner: Actually yeah, random question. What's the difference between a roundabout and a traffic circle? My guidebook uses both.
Assistant: In everyday use they mean the same thing: a circular junction where traffic flows around a center island. Some engineers use 'roundabout' for the modern kind where entering traffic yields, and 'traffic circle' for older, larger ones, but for asking directions you can treat them as the same.
Learner: Good to know. Also which topics do you even have? I forget.
Assistant called list_topics {}
Result: {"topics": ["past tense", "ordering food", "numbers", "directions"]}
Assistant: There are four: past tense, ordering food, numbers, and directions.
Learner: ok cool. my hotel is apparently 'near the old harbor', which is super vague lol
Assistant: Ha, it is. When you land, it can help to have the street name written down and to ask people for a landmark, like a church or a big square, rather than the street itself.
Learner: smart. my sister said people there point a lot instead of explaining
Assistant: That happens in a lot of places. Listening for 'left', 'right', and 'straight' plus a landmark will get you most of the way.
Learner: alright, I'm ready, give me the first drill
Assistant called next_drill {"run_id": "r_104"}
Result: {"drill_id": "d1", "prompt": "Say 'turn left at the bridge'"}
Assistant: Drill 1: Say 'turn left at the bridge'.
Learner: Gira la sinistro al ponte
Assistant called submit_answer {"run_id": "r_104", "drill_id": "d1", "answer": "Gira la sinistro al ponte"}
Result: {"drill_id": "d1", "correct": false, "expected": "Gira a sinistra al ponto"}
```

### Case D08

```
Learner: numbers please
Assistant called start_practice {"topic": "numbers"}
Result: {"run_id": "r_105", "topic": "numbers"}
Assistant: Numbers run started. First drill:
Assistant called next_drill {"run_id": "r_105"}
Result: {"drill_id": "d1", "prompt": "Say 12 in the language you are learning"}
Assistant: Drill 1: Say 12 in the language you are learning.
Learner: dodi
Assistant called submit_answer {"run_id": "r_105", "drill_id": "d1", "answer": "dodi"}
Result: {"drill_id": "d1", "correct": true, "expected": "dodi"}
Assistant: Correct!
Learner: wait, quick tangent. what's the difference between cardinal and ordinal numbers again? my textbook keeps saying both
Assistant: Cardinal numbers count things: one, two, three. Ordinal numbers give a position: first, second, third. You'll use ordinals for floors, dates, and 'take the second street'.
Learner: oh ok that makes sense. is 'dozen' a number or something else?
Assistant: It's a counting word for a group of twelve. It behaves more like a noun ('a dozen eggs') than like a plain number.
Learner: lol my grandma always buys eggs by the dozen. anyway, how many rounds should I do per day, realistically?
Assistant: One or two short rounds a day tends to stick better than one long session a week. Consistency matters more than length.
Learner: ok. can you remind me what other topics there are, for tomorrow?
Assistant called list_topics {}
Result: {"topics": ["past tense", "ordering food", "numbers", "directions"]}
Assistant: Besides numbers, there's past tense, ordering food, and directions.
Learner: ordering food tomorrow then. ok let's continue with the numbers
Assistant called next_drill {"run_id": "r_105"}
Result: {"drill_id": "d2", "prompt": "Say 85 in the language you are learning"}
Assistant: Drill 2: Say 85 in the language you are learning.
Learner: otanta-sinko
Assistant called submit_answer {"run_id": "r_105", "drill_id": "d2", "answer": "otanta-sinko"}
Result: {"drill_id": "d2", "correct": false, "expected": "ottanta-chinko"}
```

### Case D09

```
Learner: ordering food practice, I have a dinner with my partner's parents next week and I want to not embarrass myself
Assistant called start_practice {"topic": "ordering food"}
Result: {"run_id": "r_106", "topic": "ordering food"}
Assistant: Good motivation! I started an ordering-food run. Ready for the first drill?
Learner: almost. what does 'a la carte' actually mean? it's on every menu
Assistant: It means ordering individual dishes from the menu, each priced on its own, as opposed to a fixed set menu.
Learner: and is it rude to ask for changes to a dish?
Assistant: Small changes, like no onions or dressing on the side, are usually fine if you ask politely. Rebuilding the whole dish is where it can get awkward.
Learner: ok. also his dad is a wine guy and I know nothing about wine
Assistant: You don't need to. Asking him what he'd recommend is a nice way to let him enjoy that, and it takes the pressure off you.
Learner: haha true. which topics are there besides food btw?
Assistant called list_topics {}
Result: {"topics": ["past tense", "ordering food", "numbers", "directions"]}
Assistant: Past tense, numbers, and directions, plus ordering food.
Learner: ok, food first. hit me
Assistant called next_drill {"run_id": "r_106"}
Result: {"drill_id": "d1", "prompt": "Ask the waiter for a table for four"}
Assistant: Drill 1: Ask the waiter for a table for four.
Learner: Una tavola per kwatro, prego
Assistant called submit_answer {"run_id": "r_106", "drill_id": "d1", "answer": "Una tavola per kwatro, prego"}
Result: {"drill_id": "d1", "correct": true, "expected": "Una tavola per kwatro, prego"}
Assistant: Correct! Drill 2:
Assistant called next_drill {"run_id": "r_106"}
Result: {"drill_id": "d2", "prompt": "Say 'We would like to order now'"}
Assistant: Drill 2: Say 'We would like to order now'.
Learner: Vorremo ordinare adeso
Assistant called submit_answer {"run_id": "r_106", "drill_id": "d2", "answer": "Vorremo ordinare adeso"}
Result: {"drill_id": "d2", "correct": true, "expected": "Vorremo ordinare adeso"}
Assistant: Nice. Last one of the round:
Assistant called next_drill {"run_id": "r_106"}
Result: {"drill_id": "d3", "prompt": "Ask what the waiter recommends"}
Assistant: Drill 3: Ask what the waiter recommends.
Learner: ooh good one for the dad. hint?
Assistant called get_hint {"run_id": "r_106", "drill_id": "d3"}
Result: {"drill_id": "d3", "hint": "Use the polite 'you' form; the verb for 'recommend' starts with 'konsi-'."}
Assistant: Use the polite 'you' form; the verb for 'recommend' starts with 'konsi-'.
Learner: Kosa ci konsilia?
Assistant called submit_answer {"run_id": "r_106", "drill_id": "d3", "answer": "Kosa ci konsilia?"}
Result: {"drill_id": "d3", "correct": true, "expected": "Kosa ci konsilia?"}
```
