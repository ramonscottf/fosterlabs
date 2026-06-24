#!/usr/bin/env python3
# Summer Expedition — full 8-mission Grade 4 math book generator.
# Concept + word problems are hand-authored to Eureka/IM Grade 4 scope.
# Warm-up fluency is generated procedurally with COMPUTED answers (no hand-typed key arithmetic).
import random, html

# ----------------------------------------------------------------------------- helpers
def frac(n, d):
    return f'<span class="frac"><span class="n">{n}</span><span class="d">{d}</span></span>'

def blank(w=120):
    return f'<span class="blank" style="width:{w}px"></span>'

CMP = '<span class="cmpblank"></span>'

# ----------------------------------------------------------------------------- procedural warm-up
def gen_warmup(seed):
    r = random.Random(seed)
    addsub = []
    used = set()
    while len(addsub) < 6:
        a = r.randint(1100, 9400)
        b = r.randint(1050, 9400)
        op = r.choice(['+', '-'])
        if op == '-':
            a, b = max(a, b), min(a, b)
            if a == b:
                continue
            ans = a - b
        else:
            if a + b > 9999:
                continue
            ans = a + b
        key = (a, b, op)
        if key in used:
            continue
        used.add(key)
        addsub.append((f"{a:,} {op} {b:,} =", f"{ans:,}"))
    facts = []
    fused = set()
    while len([f for f in facts if f[2] == 'x']) < 3:
        x = r.randint(3, 9); y = r.randint(4, 9)
        if (x, y, 'x') in fused: continue
        fused.add((x, y, 'x'))
        facts.append((f"{x} \u00d7 {y} =", str(x * y), 'x'))
    while len([f for f in facts if f[2] == 'd']) < 3:
        q = r.randint(4, 9); x = r.randint(4, 9)
        prod = q * x
        if (prod, x, 'd') in fused: continue
        fused.add((prod, x, 'd'))
        facts.append((f"{prod} \u00f7 {x} =", str(q), 'd'))
    facts = [f[:2] for f in facts]
    return addsub, facts

# ----------------------------------------------------------------------------- mission content
MISSIONS = [
 {"no":1,
  "concept":{"k":"Objective \u00b7 Concept","title":"Place Value &amp; Rounding",
    "teach":[f'Every digit has a <b>place</b>, and its place tells you its <b>value</b>. In <span class="ex">27,418</span>, the <b>7</b> sits in the thousands place \u2014 so its value is <span class="ex">7,000</span>, not just 7.',
             f'To <b>round</b>, look at the digit just to the <b>right</b> of the place you want. 5 or more rounds up; 4 or less stays put. Rounding <span class="ex">4,827</span> to the nearest hundred \u2192 look at the 2 \u2192 <span class="ex">4,800</span>.'],
    "q":[
      {"h":f'What is the <b>value</b> of the digit <span class="mono">7</span> in <span class="mono">73,482</span>?', "tag":f'Value: {blank()}', "ans":"70,000"},
      {"h":f'Write this number in standard form: <span class="mono">60,000 + 3,000 + 200 + 50 + 4</span>', "tag":f'Standard form: {blank()}', "ans":"63,254"},
      {"h":f'Round <span class="mono">4,827</span> to the nearest <b>hundred</b>, then the nearest <b>thousand</b>.', "tag":f'Hundred: {blank(90)} &nbsp; Thousand: {blank(90)}', "ans":"4,800 ; 5,000"},
      {"h":f'Round <span class="mono">38,461</span> to the nearest <b>thousand</b>, then the nearest <b>ten thousand</b>.', "tag":f'Thousand: {blank(90)} &nbsp; Ten thousand: {blank(90)}', "ans":"38,000 ; 40,000"},
      {"h":f'Write <span class="mono">&lt;</span>, <span class="mono">&gt;</span>, or <span class="mono">=</span>: &nbsp; <span class="mono">12,405</span> {CMP} <span class="mono">12,450</span>', "ans":"12,405 &lt; 12,450"},
      {"h":f'Put these in order from <b>least to greatest</b>: &nbsp; <span class="mono">9,870 &nbsp; 9,087 &nbsp; 9,807 &nbsp; 9,078</span>', "box":"short", "ans":"9,078 \u00b7 9,087 \u00b7 9,807 \u00b7 9,870"},
    ]},
  "word":{"title":"Out on the Trail",
    "q":[
      {"h":f'The expedition packs <span class="mono">1,250</span> ration bars on Monday and <span class="mono">1,875</span> more on Tuesday. The crew eats <span class="mono">940</span> on the trail. How many ration bars are left?', "ans":"1,250 + 1,875 = 3,125; 3,125 \u2212 940 = <b>2,185 bars</b>"},
      {"h":f'Rover A logs <span class="mono">3,408</span> meters. Rover B travels <span class="mono">1,756</span> meters <b>more</b> than Rover A. How far did Rover B travel?', "ans":"3,408 + 1,756 = <b>5,164 meters</b>"},
      {"h":f'A satellite can store <span class="mono">8,000</span> photos and has taken <span class="mono">5,640</span>. <b>About</b> how many can it still take? Round to the nearest <b>hundred</b>.', "ans":"8,000 \u2212 5,640 = 2,360 \u2192 <b>2,400 photos</b>"},
    ]},
  "bender":{"title":"The Supply Drop",
    "h":f'Mission Control needs to split <span class="bmono">4,824</span> supply crates <b>evenly</b> among <b>6</b> landing zones. How many crates go to each zone? Then, if one zone hands <b>150</b> crates to a neighbor, how many does the neighbor end up with?',
    "ans":["4,824 \u00f7 6 = <b>804 crates</b> per zone", "804 + 150 = <b>954 crates</b> for the neighbor"],
    "note":"Reaches toward 5th-grade multi-step reasoning \u2014 no pressure if skipped."}},

 {"no":2,
  "concept":{"k":"Objective \u00b7 Concept","title":"Measurement &amp; Units",
    "teach":[f'Metric units step by powers of ten. Memorize these: <span class="ex">1 km = 1,000 m</span>, <span class="ex">1 m = 100 cm</span>, <span class="ex">1 kg = 1,000 g</span>, <span class="ex">1 L = 1,000 mL</span>.',
             f'Going from a <b>big</b> unit to a <b>small</b> one, you multiply. So 3 km becomes 3 \u00d7 1,000 = <span class="ex">3,000 m</span>.'],
    "q":[
      {"h":f'<span class="mono">3 km</span> = <span class="mono">?</span> m', "tag":f'{blank(90)} m', "ans":"3,000 m"},
      {"h":f'<span class="mono">5 m</span> = <span class="mono">?</span> cm', "tag":f'{blank(90)} cm', "ans":"500 cm"},
      {"h":f'<span class="mono">4 kg</span> = <span class="mono">?</span> g', "tag":f'{blank(90)} g', "ans":"4,000 g"},
      {"h":f'<span class="mono">2 L</span> = <span class="mono">?</span> mL', "tag":f'{blank(90)} mL', "ans":"2,000 mL"},
      {"h":f'<span class="mono">7 km 250 m</span> = <span class="mono">?</span> m', "tag":f'{blank(90)} m', "ans":"7,250 m"},
      {"h":f'<span class="mono">6,000 mL</span> = <span class="mono">?</span> L', "tag":f'{blank(90)} L', "ans":"6 L"},
    ]},
  "word":{"title":"Measuring the Mission",
    "q":[
      {"h":f'A trail is <span class="mono">8 km</span> long. The crew hikes <span class="mono">3 km 600 m</span> before lunch. How many <b>meters</b> are left to go?', "ans":"8,000 \u2212 3,600 = <b>4,400 m</b>"},
      {"h":f'Each canister holds <span class="mono">2 L</span> of water. The crew fills <span class="mono">5</span> canisters. How many <b>mL</b> of water is that in total?', "ans":"2,000 \u00d7 5 = <b>10,000 mL</b>"},
      {"h":f'A supply crate has a mass of <span class="mono">3 kg</span>. There are <span class="mono">4</span> crates. What is the total mass in <b>grams</b>?', "ans":"3,000 \u00d7 4 = <b>12,000 g</b>"},
    ]},
  "bender":{"title":"The Fuel Gauge",
    "h":f'The rover\u2019s tank holds <span class="bmono">6 L</span> of fuel. It burns <span class="bmono">750 mL</span> every hour. After <b>7 hours</b>, how many <b>mL</b> of fuel are left?',
    "ans":["6 L = 6,000 mL", "750 \u00d7 7 = 5,250 mL used", "6,000 \u2212 5,250 = <b>750 mL left</b>"],
    "note":"Mixed units + multiply + subtract."}},

 {"no":3,
  "concept":{"k":"Objective \u00b7 Concept","title":"Multiply Big Numbers",
    "teach":[f'Break a big multiply into <b>parts</b>. For <span class="ex">8 \u00d7 47</span>, do 8 \u00d7 40 = 320 and 8 \u00d7 7 = 56, then add: 320 + 56 = <span class="ex">376</span>.',
             f'For a 2-digit \u00d7 2-digit like <span class="ex">23 \u00d7 14</span>, multiply by the ones, then the tens, then add. Stack it neatly and line up your places.'],
    "q":[
      {"h":f'<span class="mono">34 \u00d7 6</span> =', "tag":f'{blank(90)}', "ans":"204"},
      {"h":f'<span class="mono">8 \u00d7 47</span> =', "tag":f'{blank(90)}', "ans":"376"},
      {"h":f'<span class="mono">213 \u00d7 4</span> =', "tag":f'{blank(90)}', "ans":"852"},
      {"h":f'<span class="mono">5 \u00d7 1,206</span> =', "tag":f'{blank(90)}', "ans":"6,030"},
      {"h":f'<span class="mono">23 \u00d7 14</span> =', "tag":f'{blank(90)}', "ans":"322"},
      {"h":f'<span class="mono">36 \u00d7 25</span> =', "tag":f'{blank(90)}', "ans":"900"},
    ]},
  "word":{"title":"Scaling Up",
    "q":[
      {"h":f'Each supply pod holds <span class="mono">144</span> items. The expedition has <span class="mono">6</span> pods. How many items in total?', "ans":"144 \u00d7 6 = <b>864 items</b>"},
      {"h":f'A solar panel makes <span class="mono">235</span> watts. How many watts do <span class="mono">4</span> panels make together?', "ans":"235 \u00d7 4 = <b>940 watts</b>"},
      {"h":f'The base has <span class="mono">18</span> rows of seats with <span class="mono">15</span> seats in each row. How many seats are there?', "ans":"18 \u00d7 15 = <b>270 seats</b>"},
    ]},
  "bender":{"title":"The Drone Run",
    "h":f'A drone flies <span class="bmono">1,250</span> meters per trip. It makes <b>8 trips</b> a day for <b>3 days</b>. How many meters does it fly in all?',
    "ans":["1,250 \u00d7 8 = 10,000 m per day", "10,000 \u00d7 3 = <b>30,000 meters</b>"],
    "note":"Two multiplications in a row \u2014 nice and tidy."}},

 {"no":4,
  "concept":{"k":"Objective \u00b7 Concept","title":"Division &amp; Remainders",
    "teach":[f'Division splits a number into equal groups. Sometimes there\u2019s a leftover \u2014 the <b>remainder</b>. <span class="ex">48 \u00f7 5 = 9 R3</span> means 9 groups of 5, with 3 left over.',
             f'Check your work by multiplying back: 9 \u00d7 5 = 45, plus the remainder 3 = 48. \u2713'],
    "q":[
      {"h":f'<span class="mono">48 \u00f7 5</span> =', "tag":f'{blank(90)}', "ans":"9 R3"},
      {"h":f'<span class="mono">76 \u00f7 4</span> =', "tag":f'{blank(90)}', "ans":"19"},
      {"h":f'<span class="mono">95 \u00f7 8</span> =', "tag":f'{blank(90)}', "ans":"11 R7"},
      {"h":f'<span class="mono">128 \u00f7 6</span> =', "tag":f'{blank(90)}', "ans":"21 R2"},
      {"h":f'<span class="mono">405 \u00f7 5</span> =', "tag":f'{blank(90)}', "ans":"81"},
      {"h":f'<span class="mono">738 \u00f7 9</span> =', "tag":f'{blank(90)}', "ans":"82"},
    ]},
  "word":{"title":"Sharing the Load",
    "q":[
      {"h":f'<span class="mono">50</span> ration bars are shared equally among <span class="mono">6</span> crew members. How many does each get, and how many are left over?', "ans":"50 \u00f7 6 = 8 R2 \u2192 <b>8 each, 2 left over</b>"},
      {"h":f'A transport van holds <span class="mono">9</span> people. <span class="mono">75</span> explorers need a ride. How many vans are needed so <b>everyone</b> fits?', "ans":"75 \u00f7 9 = 8 R3 \u2192 need <b>9 vans</b> (the leftover 3 still need a ride)"},
      {"h":f'<span class="mono">144</span> batteries are packed <span class="mono">8</span> to a box. How many <b>full</b> boxes can be packed?', "ans":"144 \u00f7 8 = <b>18 boxes</b>"},
    ]},
  "bender":{"title":"The Seed Field",
    "h":f'<span class="bmono">2,556</span> seeds are planted in <b>9</b> equal rows. How many seeds per row? Then the crew adds <b>4 more</b> rows with the same number each \u2014 how many seeds do the new rows need?',
    "ans":["2,556 \u00f7 9 = <b>284 seeds</b> per row", "284 \u00d7 4 = <b>1,136 seeds</b> for the new rows"],
    "note":"Divide, then multiply \u2014 two skills in one."}},

 {"no":5,
  "concept":{"k":"Objective \u00b7 Concept","title":"Angles &amp; Shapes",
    "teach":[f'Angles are measured in <b>degrees</b>. A <span class="ex">right angle = 90\u00b0</span>, a <span class="ex">straight angle = 180\u00b0</span>. Smaller than 90\u00b0 is <b>acute</b>; between 90\u00b0 and 180\u00b0 is <b>obtuse</b>.',
             f'Angles on a straight line add up to <span class="ex">180\u00b0</span>. Angles all the way around a point add up to <span class="ex">360\u00b0</span>.'],
    "q":[
      {"h":f'An angle measures <span class="mono">45\u00b0</span>. Is it acute, right, or obtuse?', "tag":f'{blank(110)}', "ans":"acute"},
      {"h":f'An angle measures <span class="mono">130\u00b0</span>. Is it acute, right, or obtuse?', "tag":f'{blank(110)}', "ans":"obtuse"},
      {"h":f'Two angles sit on a <b>straight line</b>. One is <span class="mono">65\u00b0</span>. What is the other?', "tag":f'{blank(90)}', "ans":"115\u00b0 (180 \u2212 65)"},
      {"h":f'A <b>right angle</b> is split into two parts. One part is <span class="mono">30\u00b0</span>. What is the other?', "tag":f'{blank(90)}', "ans":"60\u00b0 (90 \u2212 30)"},
      {"h":f'How many <b>lines of symmetry</b> does a square have?', "tag":f'{blank(90)}', "ans":"4"},
      {"h":f'A triangle has angles <span class="mono">90\u00b0, 45\u00b0, 45\u00b0</span>. What type is it (by its angles)?', "tag":f'{blank(120)}', "ans":"a right triangle"},
    ]},
  "word":{"title":"Turning &amp; Tilting",
    "q":[
      {"h":f'A camp flag turns from pointing <b>north</b> to pointing <b>east</b>. How many degrees did it turn?', "ans":"a quarter turn = <b>90\u00b0</b>"},
      {"h":f'A solar panel tilts <span class="mono">35\u00b0</span>, then tilts <span class="mono">20\u00b0</span> more. What is its total tilt angle?', "ans":"35 + 20 = <b>55\u00b0</b>"},
      {"h":f'Three angles meet around a point: <span class="mono">120\u00b0</span>, <span class="mono">140\u00b0</span>, and one more. What is the third angle?', "ans":"360 \u2212 (120 + 140) = <b>100\u00b0</b>"},
    ]},
  "bender":{"title":"The Square Patrol",
    "h":f'An explorer walks, then turns <b>90\u00b0</b>, walks, turns <b>90\u00b0</b>, and keeps going until they\u2019ve made <b>four</b> turns of 90\u00b0. How many degrees did they turn in total, and which way are they facing compared to the start?',
    "ans":["4 \u00d7 90\u00b0 = <b>360\u00b0</b> total", "Facing the <b>same direction</b> as the start (a full circle)"],
    "note":"Geometry reasoning, not just arithmetic."}},

 {"no":6,
  "concept":{"k":"Objective \u00b7 Concept","title":"Fractions",
    "teach":[f'<b>Equivalent</b> fractions name the same amount. Multiply the top and bottom by the same number: {frac(1,2)} = {frac(2,4)} = {frac(4,8)}.',
             f'To <b>add or subtract</b> fractions with the <b>same</b> denominator, just add or subtract the tops and keep the bottom: {frac(3,8)} + {frac(2,8)} = {frac(5,8)}.'],
    "q":[
      {"h":f'Fill in the equivalent fraction: &nbsp; {frac(1,2)} = {frac("?",8)}', "tag":f'top number: {blank(70)}', "ans":frac(4,8)},
      {"h":f'Fill in the equivalent fraction: &nbsp; {frac(2,3)} = {frac("?",12)}', "tag":f'top number: {blank(70)}', "ans":frac(8,12)},
      {"h":f'Compare with &lt;, &gt;, or =: &nbsp; {frac(3,4)} {CMP} {frac(2,4)}', "ans":f'{frac(3,4)} &gt; {frac(2,4)}'},
      {"h":f'Compare with &lt;, &gt;, or =: &nbsp; {frac(1,3)} {CMP} {frac(1,2)}', "ans":f'{frac(1,3)} &lt; {frac(1,2)}'},
      {"h":f'{frac(3,8)} + {frac(2,8)} =', "tag":f'{blank(70)}', "ans":frac(5,8)},
      {"h":f'{frac(5,6)} \u2212 {frac(2,6)} =', "tag":f'{blank(70)}', "ans":f'{frac(3,6)} (same as {frac(1,2)})'},
    ]},
  "word":{"title":"Slices of the Mission",
    "q":[
      {"h":f'The crew eats {frac(3,8)} of a ration pack in the morning and {frac(2,8)} at night. How much did they eat in all?', "ans":f'{frac(3,8)} + {frac(2,8)} = <b>{frac(5,8)}</b>'},
      {"h":f'A water tank is {frac(7,10)} full. The crew uses {frac(4,10)} of the tank. How much is left?', "ans":f'{frac(7,10)} \u2212 {frac(4,10)} = <b>{frac(3,10)}</b>'},
      {"h":f'Each scoop is {frac(1,4)} of a liter. The cook uses <span class="mono">3</span> scoops. How many liters is that?', "ans":f'3 \u00d7 {frac(1,4)} = <b>{frac(3,4)} L</b>'},
    ]},
  "bender":{"title":"The Long Trail",
    "h":f'A trail is divided into <b>12</b> equal segments. The crew finishes <b>8</b> of them. Write the fraction <b>completed</b>, then the fraction <b>left</b>, then say which is bigger.',
    "ans":[f'Completed = {frac(8,12)}, &nbsp; Left = {frac(4,12)}', f'{frac(8,12)} &gt; {frac(4,12)} \u2014 more is done than left'],
    "note":"Reading a situation as fractions."}},

 {"no":7,
  "concept":{"k":"Objective \u00b7 Concept","title":"Decimals",
    "teach":[f'Decimals are another way to write tenths and hundredths. <span class="ex">{frac(1,10)} = 0.1</span> and <span class="ex">{frac(1,100)} = 0.01</span>. So {frac(7,10)} = <span class="ex">0.7</span>.',
             f'To <b>compare</b> decimals, line up the decimal points and compare place by place. Remember 0.30 and 0.3 are <b>equal</b>.'],
    "q":[
      {"h":f'Write {frac(7,10)} as a decimal.', "tag":f'{blank(90)}', "ans":"0.7"},
      {"h":f'Write <span class="mono">0.45</span> as a fraction.', "tag":f'{blank(90)}', "ans":frac(45,100)},
      {"h":f'Write {frac(3,100)} as a decimal.', "tag":f'{blank(90)}', "ans":"0.03"},
      {"h":f'Compare with &lt;, &gt;, or =: &nbsp; <span class="mono">0.6</span> {CMP} <span class="mono">0.45</span>', "ans":"0.6 &gt; 0.45"},
      {"h":f'Compare with &lt;, &gt;, or =: &nbsp; <span class="mono">0.30</span> {CMP} <span class="mono">0.3</span>', "ans":"0.30 = 0.3"},
      {"h":f'<span class="mono">0.4 + 0.5</span> =', "tag":f'{blank(90)}', "ans":"0.9"},
    ]},
  "word":{"title":"Decimal Readings",
    "q":[
      {"h":f'A coin is <span class="mono">0.2 cm</span> thick. If you stack <span class="mono">4</span> coins, how tall is the stack?', "ans":"0.2 \u00d7 4 = <b>0.8 cm</b>"},
      {"h":f'The rover traveled <span class="mono">1.5 km</span>, then <span class="mono">2.3 km</span> more. How far did it travel in all?', "ans":"1.5 + 2.3 = <b>3.8 km</b>"},
      {"h":f'One beaker holds <span class="mono">0.75 L</span>. Another holds <span class="mono">0.50 L</span>. How much <b>more</b> does the first hold?', "ans":"0.75 \u2212 0.50 = <b>0.25 L</b>"},
    ]},
  "bender":{"title":"The Sample Weights",
    "h":f'A rock sample weighs <span class="bmono">0.6 kg</span>. Mission Control collects <b>3</b> of them. What is the total weight? Then, how much <b>more</b> is needed to reach <b>2 kg</b>?',
    "ans":["0.6 \u00d7 3 = <b>1.8 kg</b> total", "2.0 \u2212 1.8 = <b>0.2 kg</b> more needed"],
    "note":"Multiply decimals, then subtract."}},

 {"no":8,
  "concept":{"k":"Objective \u00b7 Mixed Review","title":"Everything You\u2019ve Cleared",
    "teach":[f'This is the <b>Final Expedition</b>. One problem from every mission this summer. You\u2019ve done every one of these before \u2014 this is your victory lap.'],
    "q":[
      {"h":f'<b>Rounding:</b> Round <span class="mono">6,748</span> to the nearest <b>hundred</b>.', "tag":f'{blank(90)}', "ans":"6,700"},
      {"h":f'<b>Units:</b> <span class="mono">5 km</span> = <span class="mono">?</span> m', "tag":f'{blank(90)} m', "ans":"5,000 m"},
      {"h":f'<b>Multiply:</b> <span class="mono">124 \u00d7 3</span> =', "tag":f'{blank(90)}', "ans":"372"},
      {"h":f'<b>Divide:</b> <span class="mono">99 \u00f7 8</span> =', "tag":f'{blank(90)}', "ans":"12 R3"},
      {"h":f'<b>Fractions:</b> {frac(2,5)} + {frac(1,5)} =', "tag":f'{blank(70)}', "ans":frac(3,5)},
      {"h":f'<b>Decimals:</b> Compare &lt;, &gt;, or =: &nbsp; <span class="mono">0.7</span> {CMP} <span class="mono">0.65</span>', "ans":"0.7 &gt; 0.65"},
    ]},
  "word":{"title":"The Last Push",
    "q":[
      {"h":f'The crew packs <span class="mono">6</span> crates with <span class="mono">125</span> items each, then gives away <span class="mono">248</span> items. <b>About</b> how many are left? Round to the nearest <b>hundred</b>.', "ans":"6 \u00d7 125 = 750; 750 \u2212 248 = 502 \u2192 <b>500 items</b>"},
      {"h":f'A <span class="mono">4 L</span> tank is split equally into <span class="mono">8</span> bottles. How many <b>mL</b> go in each bottle?', "ans":"4 L = 4,000 mL; 4,000 \u00f7 8 = <b>500 mL each</b>"},
      {"h":f'The trail is <span class="mono">2.5 km</span> long. The crew walks the whole thing <span class="mono">3</span> times. How many km is that?', "ans":"2.5 \u00d7 3 = <b>7.5 km</b>"},
    ]},
  "bender":{"title":"Final Expedition: The Storm",
    "h":f'The base has <span class="bmono">1,000</span> supply units. It sends out <b>6</b> teams, each taking <b>84</b> units. Then a storm destroys <b>one quarter</b> of what\u2019s <b>left</b>. How many supply units remain?',
    "ans":["6 \u00d7 84 = 504 units sent out", "1,000 \u2212 504 = 496 units left", "\u00bc of 496 = 124 destroyed", "496 \u2212 124 = <b>372 units remain</b>"],
    "note":"The capstone \u2014 multiply, subtract, and a fraction of a whole, all in one."}},
]

MAP = [(1,"Place Value &amp; Rounding"),(2,"Measurement &amp; Units"),(3,"Multiply Big Numbers"),
       (4,"Division &amp; Remainders"),(5,"Angles &amp; Shapes"),(6,"Fractions"),
       (7,"Decimals"),(8,"Final Expedition")]

# ----------------------------------------------------------------------------- CSS
CSS = """
:root{--navy:#0E1B2A;--navy-soft:#16293d;--paper:#FBF9F4;--orange:#FF6B35;--teal:#1FB8A6;--slate:#5B6B7B;--sky:#DCEEF5;--ink:#16202b;--line:#d7dde3;}
*{box-sizing:border-box;-webkit-print-color-adjust:exact;print-color-adjust:exact;}
html,body{margin:0;padding:0;}
body{background:#fff;font-family:'Nunito',sans-serif;color:var(--ink);line-height:1.5;}
.page{padding:0;page-break-after:always;break-after:page;}
.page:last-child{page-break-after:auto;}
.cover{background:var(--navy);color:#fff;display:flex;flex-direction:column;min-height:9.4in;padding:60px 58px;}
.cover .topcode{font-family:'Space Mono',monospace;font-size:13px;letter-spacing:.18em;color:var(--teal);text-transform:uppercase;display:flex;justify-content:space-between;border-bottom:1px solid rgba(255,255,255,.18);padding-bottom:14px;}
.route{margin:46px 0 8px;height:74px;}
.route svg{width:100%;height:100%;overflow:visible;}
.cover .lockup{margin-top:auto;}
.cover .eyebrow{font-family:'Space Mono',monospace;font-size:14px;letter-spacing:.32em;color:var(--orange);text-transform:uppercase;margin:0 0 10px;}
.cover h1{font-family:'Baloo 2',cursive;font-weight:800;font-size:88px;line-height:.92;margin:0;letter-spacing:-.01em;}
.cover h1 .row2{color:var(--orange);display:block;}
.cover .sub{font-size:20px;color:#cfe0ec;margin:22px 0 0;max-width:34ch;font-weight:600;}
.cover .commander{margin-top:34px;padding-top:24px;border-top:1px solid rgba(255,255,255,.18);display:flex;align-items:flex-end;justify-content:space-between;gap:20px;flex-wrap:wrap;}
.cover .commander .label{font-family:'Space Mono',monospace;font-size:12px;letter-spacing:.14em;color:var(--teal);text-transform:uppercase;margin:0 0 4px;}
.cover .commander .name{font-family:'Baloo 2',cursive;font-weight:700;font-size:36px;line-height:1;color:#fff;}
.patch{width:128px;height:128px;flex:none;border-radius:50%;background:radial-gradient(circle at 50% 38%,var(--navy-soft),#0a141f);border:3px solid var(--orange);display:flex;flex-direction:column;align-items:center;justify-content:center;box-shadow:0 0 0 6px rgba(255,107,53,.12);text-align:center;}
.patch .pk{font-family:'Space Mono',monospace;font-size:11px;letter-spacing:.2em;color:var(--teal);}
.patch .pg{font-family:'Baloo 2',cursive;font-weight:800;font-size:40px;line-height:.9;color:#fff;}
.patch .pl{font-family:'Space Mono',monospace;font-size:10px;letter-spacing:.16em;color:#cfe0ec;}
.phead{display:flex;align-items:center;gap:16px;margin-bottom:22px;padding-bottom:16px;border-bottom:3px solid var(--navy);}
.phead .mno{font-family:'Space Mono',monospace;font-weight:700;font-size:13px;color:#fff;background:var(--navy);padding:7px 12px;border-radius:8px;letter-spacing:.08em;white-space:nowrap;}
.phead .ptitle{flex:1;}
.phead .ptitle .k{font-family:'Space Mono',monospace;font-size:12px;letter-spacing:.16em;color:var(--orange);text-transform:uppercase;margin:0 0 2px;}
.phead .ptitle h2{font-family:'Baloo 2',cursive;font-weight:700;font-size:29px;margin:0;line-height:1;color:var(--navy);}
.phead .stamp-slot{font-family:'Space Mono',monospace;font-size:11px;color:var(--slate);border:2px dashed var(--line);border-radius:10px;padding:8px 12px;text-align:center;line-height:1.3;white-space:nowrap;}
.phead .stamp-slot b{display:block;color:var(--teal);font-size:13px;}
.briefing h2.big{font-family:'Baloo 2',cursive;font-weight:800;font-size:38px;color:var(--navy);margin:0 0 6px;line-height:1;}
.briefing .lede{font-size:18px;color:var(--slate);font-weight:700;margin:0 0 26px;}
.rules{list-style:none;margin:0 0 28px;padding:0;}
.rules li{display:flex;gap:14px;align-items:flex-start;padding:13px 0;border-top:1px solid var(--line);font-size:16px;}
.rules li:last-child{border-bottom:1px solid var(--line);}
.rules .num{font-family:'Space Mono',monospace;font-weight:700;font-size:13px;color:#fff;background:var(--teal);border-radius:50%;width:30px;height:30px;flex:none;display:flex;align-items:center;justify-content:center;}
.rules b{color:var(--navy);}
.callout{background:var(--sky);border-left:5px solid var(--teal);border-radius:0 12px 12px 0;padding:17px 22px;font-size:16px;color:var(--navy);font-weight:600;}
.callout .ct{font-family:'Space Mono',monospace;font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--teal);display:block;margin-bottom:5px;}
.maptitle{font-family:'Space Mono',monospace;font-size:13px;letter-spacing:.16em;text-transform:uppercase;color:var(--orange);margin:34px 0 4px;}
.mapsub{font-size:15px;color:var(--slate);margin:0 0 20px;font-weight:600;}
.missiongrid{display:grid;grid-template-columns:repeat(4,1fr);gap:18px 16px;}
.mtile{text-align:center;}
.mbadge{width:74px;height:74px;margin:0 auto 8px;border-radius:50%;border:2.5px solid var(--line);background:#fff;display:flex;align-items:center;justify-content:center;font-family:'Baloo 2',cursive;font-weight:800;font-size:28px;color:var(--line);}
.mtile .ml{font-family:'Space Mono',monospace;font-size:11px;color:var(--slate);letter-spacing:.04em;}
.mtile .mt{font-size:13px;font-weight:700;color:var(--navy);line-height:1.2;margin-top:2px;}
.mtile .clr{font-family:'Space Mono',monospace;font-size:10px;color:var(--slate);margin-top:6px;display:flex;align-items:center;justify-content:center;gap:5px;}
.chk{width:13px;height:13px;border:1.5px solid var(--slate);border-radius:3px;display:inline-block;}
.lead{font-size:16px;color:var(--slate);margin:0 0 12px;font-weight:600;}
.lead b{color:var(--navy);}
.teach{background:var(--paper);border:1px solid var(--line);border-radius:14px;padding:15px 20px;margin:0 0 18px;break-inside:avoid;}
.teach .tk{font-family:'Space Mono',monospace;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--teal);margin:0 0 8px;}
.teach p{margin:0 0 8px;font-size:16px;}
.teach p:last-child{margin-bottom:0;}
.teach .ex{font-family:'Space Mono',monospace;font-weight:700;color:var(--navy);}
.drill{display:grid;grid-template-columns:repeat(2,1fr);gap:12px 30px;margin-bottom:8px;}
.drow{display:flex;align-items:center;gap:12px;padding:12px 0;border-bottom:1px solid var(--line);break-inside:avoid;}
.qn{font-family:'Space Mono',monospace;font-weight:700;font-size:13px;color:#fff;background:var(--navy);border-radius:7px;width:30px;height:30px;flex:none;display:flex;align-items:center;justify-content:center;}
.qx{font-family:'Space Mono',monospace;font-size:20px;font-weight:700;color:var(--ink);flex:1;}
.ansline{width:78px;border-bottom:2px solid var(--slate);height:24px;flex:none;}
.qlist{list-style:none;margin:0;padding:0;}
.qlist>li{display:flex;gap:14px;padding:11px 0;border-bottom:1px solid var(--line);break-inside:avoid;}
.qlist>li:first-child{border-top:1px solid var(--line);}
.qbody{flex:1;}
.qbody .qt{font-size:16px;margin:0 0 10px;}
.qbody .qt .mono{font-family:'Space Mono',monospace;font-weight:700;}
.writebox{border:1.5px dashed var(--line);border-radius:10px;height:45px;}
.writebox.short{height:40px;}
.answertag{font-family:'Space Mono',monospace;font-size:12px;color:var(--slate);display:inline-flex;align-items:center;gap:8px;margin-top:8px;flex-wrap:wrap;}
.blank{display:inline-block;border-bottom:2px solid var(--slate);height:22px;vertical-align:bottom;}
.cmpblank{display:inline-block;width:44px;border-bottom:2px solid var(--slate);height:22px;vertical-align:bottom;margin:0 4px;}
.frac{display:inline-flex;flex-direction:column;text-align:center;vertical-align:middle;margin:0 3px;font-family:'Space Mono',monospace;font-weight:700;line-height:1.05;}
.frac .n{padding:0 5px;}
.frac .d{padding:1px 5px 0;border-top:2px solid currentColor;}
.bender{background:var(--navy);color:#fff;border-radius:16px;padding:16px 24px;margin-top:6px;break-inside:avoid;}
.bender .bk{font-family:'Space Mono',monospace;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--orange);margin:0 0 8px;}
.bender h3{font-family:'Baloo 2',cursive;font-weight:700;font-size:22px;margin:0 0 8px;}
.bender p{font-size:16px;color:#dbe7f0;margin:0 0 10px;}
.bender .bmono{font-family:'Space Mono',monospace;font-weight:700;color:#fff;}
.bender .bwrite{background:rgba(255,255,255,.08);border:1.5px dashed rgba(255,255,255,.35);border-radius:10px;height:46px;}
.bender .badge{font-size:12px;color:var(--teal);font-family:'Space Mono',monospace;margin-top:12px;margin-bottom:0;}
.keyhead{border-bottom-color:var(--teal);}
.keyhead .mno{background:var(--teal);}
.keygrid{columns:2;column-gap:44px;}
.keyblock{break-inside:avoid;margin-bottom:20px;}
.keyblock h4{font-family:'Space Mono',monospace;font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--orange);border-bottom:2px solid var(--line);padding-bottom:6px;margin:0 0 10px;}
.keyblock ol,.keyblock ul{margin:0;padding-left:20px;}
.keyblock li{font-size:14.5px;padding:3px 0;}
.keyblock .mono{font-family:'Space Mono',monospace;font-weight:700;color:var(--navy);}
.keynote{font-size:13px;color:var(--slate);margin-top:8px;}
.foot{margin-top:30px;display:flex;justify-content:space-between;font-family:'Space Mono',monospace;font-size:11px;color:var(--slate);letter-spacing:.04em;border-top:1px solid var(--line);padding-top:10px;}
.cover .foot{color:rgba(255,255,255,.5);border-top-color:rgba(255,255,255,.18);}
.cert{background:var(--navy);color:#fff;min-height:9.4in;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:60px;}
.cert .ck{font-family:'Space Mono',monospace;letter-spacing:.3em;color:var(--teal);text-transform:uppercase;font-size:14px;margin:0 0 18px;}
.cert h1{font-family:'Baloo 2',cursive;font-weight:800;font-size:62px;line-height:.95;margin:0;color:#fff;}
.cert h1 em{color:var(--orange);font-style:normal;display:block;}
.cert p{font-size:19px;color:#cfe0ec;max-width:40ch;margin:24px 0 0;font-weight:600;}
.cert .sign{margin-top:48px;width:320px;border-top:2px solid rgba(255,255,255,.4);padding-top:8px;font-family:'Space Mono',monospace;font-size:12px;letter-spacing:.14em;color:var(--teal);text-transform:uppercase;}
.cert .seal{width:120px;height:120px;border-radius:50%;border:3px solid var(--orange);display:flex;align-items:center;justify-content:center;font-family:'Baloo 2',cursive;font-weight:800;font-size:18px;color:var(--orange);margin:34px auto 0;line-height:1.05;box-shadow:0 0 0 6px rgba(255,107,53,.12);}
.mapfull .missiongrid{gap:30px 22px;margin-top:6px;}.mapfull .mbadge{width:104px;height:104px;font-size:40px;border-width:3px;}.mapfull .ml{font-size:12px;}.mapfull .mt{font-size:15px;}.mapfull .clr{font-size:11px;margin-top:8px;}.maplegend{font-size:13px;color:var(--slate);border-top:1px solid var(--line);padding-top:14px;margin-top:30px;}
@media(max-width:680px){.drill{grid-template-columns:1fr;}.missiongrid{grid-template-columns:repeat(2,1fr);}.keygrid{columns:1;}}
"""

ROUTE_SVG = """<svg viewBox="0 0 700 74" preserveAspectRatio="none"><path d="M6 60 C 120 12, 200 12, 300 40 S 520 70, 694 18" fill="none" stroke="#1FB8A6" stroke-width="3" stroke-dasharray="2 9" stroke-linecap="round"/><circle cx="6" cy="60" r="7" fill="#FF6B35"/><circle cx="300" cy="40" r="6" fill="#fff"/><circle cx="694" cy="18" r="9" fill="none" stroke="#FF6B35" stroke-width="3"/><circle cx="694" cy="18" r="3.5" fill="#FF6B35"/></svg>"""

# ----------------------------------------------------------------------------- page renderers
def cover():
    return f"""<section class="page cover">
  <div class="topcode"><span>Field Logbook</span><span>Clearance &middot; Grade 4</span></div>
  <div class="route" aria-hidden="true">{ROUTE_SVG}</div>
  <div class="lockup">
    <p class="eyebrow">Summer 2026 &middot; 8 Missions</p>
    <h1>Summer<span class="row2">Expedition</span></h1>
    <p class="sub">A field logbook of math missions. Clear one objective at a time. Stamp it. Move on.</p>
    <div class="commander">
      <div><p class="label">Commanding Officer</p><div class="name">Charles</div></div>
      <div class="patch"><span class="pk">GRADE</span><span class="pg">4</span><span class="pl">EXPEDITION</span></div>
    </div>
  </div>
  <div class="foot"><span>PROJECT: SUMMER EXPEDITION</span><span>LOG 00 / 08</span></div>
</section>"""

def briefing():
    return f"""<section class="page briefing">
  <div class="phead"><span class="mno">BRIEFING</span><div class="ptitle"><p class="k">Read this first, Commander</p><h2>How the Expedition Works</h2></div></div>
  <p class="lede">You&rsquo;re not studying. You&rsquo;re running missions.</p>
  <ul class="rules">
    <li><span class="num">1</span><div><b>One objective set a day.</b> About 15 minutes. You don&rsquo;t have to clear a whole mission at once &mdash; a little every day moves you across the map.</div></li>
    <li><span class="num">2</span><div><b>There are no wrong landings.</b> Cross it out, try again. Re-trying a problem is exactly what real commanders do. Mistakes don&rsquo;t cost you anything here.</div></li>
    <li><span class="num">3</span><div><b>Clear it, then stamp it.</b> When you finish a page, mark it cleared in the corner and color in that mission on the next page. Watching the map fill up is the whole point.</div></li>
    <li><span class="num">4</span><div><b>Bonus Objectives are optional.</b> The dark &ldquo;Brain Bender&rdquo; boxes are extra credit for when you&rsquo;re feeling sharp. Skip them on a tired day &mdash; they don&rsquo;t count against you.</div></li>
  </ul>
  <div class="callout"><span class="ct">Mission Control note</span>Every mission is built at your grade level. It&rsquo;s meant to feel doable, not heavy. If a page ever feels like too much, that&rsquo;s a signal to stop for the day &mdash; not a sign you&rsquo;re behind. You set the pace.</div>
  <div class="foot"><span>BRIEFING</span><span>SUMMER EXPEDITION</span></div>
</section>"""

def map_page():
    tiles = ""
    for n, t in MAP:
        active = n == 1
        bstyle = "border-color:var(--orange);color:var(--orange);box-shadow:0 0 0 6px rgba(255,107,53,.12);" if active else ""
        tiles += f'<div class="mtile"><div class="mbadge" style="{bstyle}">{n}</div><div class="ml">MISSION 0{n}</div><div class="mt">{t}</div><div class="clr"><span class="chk"></span> Cleared</div></div>'
    return f"""<section class="page mapfull">
  <div class="phead"><span class="mno">THE MAP</span><div class="ptitle"><p class="k">Your Summer at a Glance</p><h2>The Mission Map</h2></div></div>
  <p class="lead">Eight missions, one summer. <b>Color in a badge</b> every time you clear a mission &mdash; this is your scoreboard.</p>
  <div class="missiongrid">{tiles}</div>
  <div class="maplegend">&#9670; Some missions hide a <b>Brain Bender</b> bonus objective. Clear one to earn the &#9670; Sharp Shooter mark &mdash; totally optional.</div>
  <div class="foot"><span>MISSION MAP</span><span>SUMMER EXPEDITION</span></div>
</section>"""

def warmup_page(m, addsub, facts):
    def rows(items, start):
        out = ""
        for i, (q, _) in enumerate(items):
            out += f'<div class="drow"><span class="qn">{start+i}</span><span class="qx">{q}</span><span class="ansline"></span></div>'
        return out
    return f"""<section class="page">
  <div class="phead"><span class="mno">MISSION 0{m['no']} &middot; A</span><div class="ptitle"><p class="k">Systems Check &middot; Fluency</p><h2>Warm-Up Drills</h2></div><div class="stamp-slot">CLEARED?<b>&#9634;</b></div></div>
  <p class="lead">Quick reps to warm the engines. <b>Add or subtract</b> each one, then knock out the fact checks. No timer &mdash; just steady.</p>
  <div class="drill">{rows(addsub,1)}</div>
  <p class="lead" style="margin:24px 0 12px;"><b>Fact checks.</b> Keep your multiplication and division sharp.</p>
  <div class="drill">{rows(facts,7)}</div>
  <div class="foot"><span>MISSION 0{m['no']} &middot; WARM-UP</span><span>GRADE 4</span></div>
</section>"""

def concept_page(m):
    c = m["concept"]
    teach = "".join(f"<p>{p}</p>" for p in c["teach"])
    qs = ""
    for q in c["q"]:
        inner = f'<p class="qt">{q["h"]}</p>'
        if q.get("box"):
            inner += f'<div class="writebox {q["box"]}"></div>'
        if q.get("tag"):
            inner += f'<span class="answertag">{q["tag"]}</span>'
        qs += f'<li><div class="qbody">{inner}</div></li>'
    return f"""<section class="page">
  <div class="phead"><span class="mno">MISSION 0{m['no']} &middot; B</span><div class="ptitle"><p class="k">{c['k']}</p><h2>{c['title']}</h2></div><div class="stamp-slot">CLEARED?<b>&#9634;</b></div></div>
  <div class="teach"><p class="tk">Mission Brief</p>{teach}</div>
  <ol class="qlist">{qs}</ol>
  <div class="foot"><span>MISSION 0{m['no']} &middot; CONCEPT</span><span>GRADE 4</span></div>
</section>"""

def word_page(m):
    w = m["word"]; b = m["bender"]
    qs = ""
    for q in w["q"]:
        qs += f'<li><div class="qbody"><p class="qt">{q["h"]}</p><div class="writebox"></div><span class="answertag">Answer: {blank()}</span></div></li>'
    return f"""<section class="page">
  <div class="phead"><span class="mno">MISSION 0{m['no']} &middot; C</span><div class="ptitle"><p class="k">Field Objectives &middot; Word Problems</p><h2>{w['title']}</h2></div><div class="stamp-slot">CLEARED?<b>&#9634;</b></div></div>
  <p class="lead">Real missions, real numbers. <b>Show your work</b> in the box &mdash; how you got there matters more than the answer.</p>
  <ol class="qlist">{qs}</ol>
  <div class="bender">
    <p class="bk">&#9670; Bonus Objective &middot; Brain Bender</p>
    <h3>{b['title']}</h3>
    <p>{b['h']}</p>
    <div class="bwrite"></div>
    <p class="badge">Optional &mdash; skip it on a tired day. Clearing it earns the &#9670; Sharp Shooter mark.</p>
  </div>
  <div class="foot"><span>MISSION 0{m['no']} &middot; TRAIL</span><span>GRADE 4</span></div>
</section>"""

def key_page(m, addsub, facts):
    c = m["concept"]; w = m["word"]; b = m["bender"]
    as_items = "".join(f"<li><span class='mono'>{a}</span></li>" for _, a in addsub)
    fact_str = " &nbsp; ".join(f"{i+7}) {a}" for i, (_, a) in enumerate(facts))
    con_items = "".join(f"<li>{q['ans']}</li>" for q in c["q"])
    word_items = "".join(f"<li>{q['ans']}</li>" for q in w["q"])
    bend_items = "".join(f"<li>{a}</li>" for a in b["ans"])
    return f"""<section class="page">
  <div class="phead keyhead"><span class="mno">DEBRIEF</span><div class="ptitle"><p class="k" style="color:var(--teal)">Mission 0{m['no']} &middot; Answer Key</p><h2>Mission Debrief</h2></div></div>
  <p class="lead">For Mission Control (the grown-up) &mdash; or for Charles to self-check once a page is done.</p>
  <div class="keygrid">
    <div class="keyblock"><h4>A &middot; Warm-Up Drills</h4><ol>{as_items}</ol><p class="keynote">Facts: {fact_str}</p></div>
    <div class="keyblock"><h4>B &middot; {c['title']}</h4><ol>{con_items}</ol></div>
    <div class="keyblock"><h4>C &middot; {w['title']}</h4><ol>{word_items}</ol></div>
    <div class="keyblock"><h4>&#9670; Brain Bender &middot; {b['title']}</h4><ul>{bend_items}</ul><p class="keynote">{b['note']}</p></div>
  </div>
  <div class="foot"><span>MISSION 0{m['no']} &middot; DEBRIEF</span><span>SUMMER EXPEDITION</span></div>
</section>"""

def certificate():
    return f"""<section class="page cert">
  <p class="ck">Expedition Complete</p>
  <h1>Mission<em>Accomplished</em></h1>
  <p>Commander Charles cleared all eight missions of the Summer Expedition. Every objective, every trail, and more than a few Brain Benders.</p>
  <div class="seal">GRADE&nbsp;4<br>CLEARED</div>
  <div class="sign">Signed &middot; Mission Control</div>
</section>"""

# ----------------------------------------------------------------------------- assemble
def build():
    pages = [cover(), briefing(), map_page()]
    for m in MISSIONS:
        addsub, facts = gen_warmup(4000 + m["no"])
        pages.append(warmup_page(m, addsub, facts))
        pages.append(concept_page(m))
        pages.append(word_page(m))
        pages.append(key_page(m, addsub, facts))
    pages.append(certificate())
    body = "\n".join(pages)
    doc = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<title>Summer Expedition &mdash; Grade 4 Math &middot; Commander Charles</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;600;700;800&family=Nunito:wght@400;600;700;800&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>@page{{size:letter;margin:0.5in;}}{CSS}</style></head><body>{body}</body></html>"""
    with open("book.html", "w") as f:
        f.write(doc)
    print("HTML written:", len(doc), "bytes,", len(pages), "pages")

if __name__ == "__main__":
    build()
