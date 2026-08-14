// Newest post first. Each new_blog_post.py run prepends one entry here.
const BLOG_POSTS = [
  {
    slug: "what-your-glow-era-actually-costs-you",
    categoryId: "confidence-glow",
    title: "What Your Glow Era Actually Costs You",
    excerpt: "The soft skin and quiet confidence get all the attention. Here's the real, honest price of admission nobody posts about.",
    date: "2026-08-14",
    readTime: "4 min read",
    category: "Confidence & Glow",
    tags: ["glow era", "self-care costs", "personal growth", "boundaries", "authenticity"]
  },
  {
    slug: "coconut-water-the-chic-hydration-secret",
    categoryId: "radical-self-care",
    title: "Coconut Water: The Chic Hydration Secret",
    excerpt: "Discover the elegant wellness benefits of coconut water, hydration, electrolytes, and natural glow. How this chic tropical drink supports modern wellness rituals, without the hype.",
    date: "2026-08-13",
    readTime: "4 min read",
    category: "Wellness Recipes",
    image: "images/coconut-beach-fresh.jpg",
    tags: ["coconut water", "hydration", "electrolytes", "wellness drink", "skin glow"]
  },
  {
    slug: "quantum-physics-and-self-care-lessons-in-uncertainty-and-presence",
    categoryId: "deep-self-love",
    title: "Quantum Physics and Self-Care: Lessons in Uncertainty and Presence",
    excerpt: "What quantum physics can teach us, metaphorically, about softness, presence, and letting go of the pressure to arrive fully formed in your glow era.",
    date: "2026-08-13",
    readTime: "4 min read",
    category: "Deep Self-Love",
    image: "images/quantum-meditation-glow.jpg",
    tags: ["quantum physics", "presence", "uncertainty", "self-love", "mindfulness"]
  },
  {
    slug: "sober-curious-socializing-how-to-show-up-at-events-without-the-drink-in-hand",
    categoryId: "radical-self-care",
    title: "Sober Curious Socializing: How to Show Up at Events Without the Drink in Hand",
    excerpt: "A quiet shift is happening at parties and dinners. Here's how to show up sober curious, clear-headed, grounded, and still fully part of the fun.",
    date: "2026-08-12",
    readTime: "4 min read",
    category: "Wellness",
    image: "images/golden-hour-toast.jpg",
    tags: ["sober curious", "mindful drinking", "boundaries", "confidence", "socializing"]
  },
  {
    slug: "digital-detox-and-screen-boundaries-how-to-reclaim-your-attention-and-calm",
    categoryId: "radical-self-care",
    title: "Digital Detox and Screen Boundaries: How to Reclaim Your Attention and Calm",
    excerpt: "The average person spends over six hours a day on screens. Here's what the research actually shows about screen boundaries, and how to build ones that restore your focus, sleep, and calm.",
    date: "2026-08-11",
    readTime: "6 min read",
    category: "Wellness",
    image: "images/unplugged-boat-reading.jpg",
    tags: ["digital detox", "screen time", "boundaries", "attention", "nervous system"]
  },
  {
    slug: "nervous-system-regulation-simple-daily-practices-for-calm",
    categoryId: "radical-self-care",
    title: "Nervous System Regulation: Simple Daily Practices for Calm",
    excerpt: "The #1 wellness trend of the year, explained simply. Practical, evidence-informed ways to help your nervous system shift out of alert mode and into calm.",
    date: "2026-08-10",
    readTime: "6 min read",
    category: "Wellness",
    image: "images/cozy-slippers-nervous-system.jpg",
    tags: ["nervous system regulation", "vagus nerve", "stress relief", "calm", "self-care"]
  },
  {
    slug: "breakfast-for-dinner-ricotta-pancakes-with-warm-berry-compote",
    categoryId: "radical-self-care",
    title: "Breakfast for Dinner Ricotta Pancakes with Warm Berry Compote",
    excerpt: "Fluffy ricotta pancakes with a glossy berry compote, an easy, elegant breakfast for dinner recipe that turns any weeknight into something quietly special.",
    date: "2026-08-10",
    readTime: "3 min read",
    category: "Wellness Recipes",
    image: "images/ricotta-pancakes-berry-compote.jpg",
    tags: ["breakfast for dinner", "ricotta pancakes", "berry compote", "brinner", "easy recipe"]
  },
  {
    slug: "keto-l-theanine-smoothie-for-calm-focus-and-glow",
    categoryId: "radical-self-care",
    title: "Keto L-Theanine Smoothie for Calm Focus and Glow",
    excerpt: "A creamy, low-carb smoothie with L-theanine for gentle calm, healthy fats for steady energy, and glow-supporting nutrients, no sugar crash, no jitters.",
    date: "2026-08-09",
    readTime: "4 min read",
    category: "Wellness Recipes",
    image: "images/smoothie-berries-almonds.jpg",
    tags: ["keto smoothie", "L-theanine", "low carb recipe", "wellness recipe", "calming smoothie"]
  },
  {
    slug: "vacation-spa-treatments-classic-and-modern-options-for-ultimate-pampering",
    categoryId: "radical-self-care",
    title: "Vacation Spa Treatments: Classic and Modern Options for Ultimate Pampering",
    excerpt: "From Swedish massage to float therapy, here's the full guide to spa treatments that turn your next vacation into deep, lasting relaxation.",
    date: "2026-08-08",
    readTime: "4 min read",
    category: "Wellness",
    image: "images/spa-thermal-pool-steam.jpg",
    tags: ["spa", "vacation spa", "massage", "wellness treatments", "self-care travel"]
  },
  {
    slug: "vacation-wellness-activities-yoga-meditation-and-nature-immersion-for-real-rest",
    categoryId: "radical-self-care",
    title: "Vacation Wellness Activities: Yoga, Meditation, and Nature Immersion for Real Rest",
    excerpt: "Turn your next trip into real recovery with three simple, evidence-backed practices, yoga, meditation, and nature immersion, that need no special gear and work almost anywhere.",
    date: "2026-08-08",
    readTime: "4 min read",
    category: "Wellness",
    image: "images/barefoot-shoreline-linen.jpg",
    tags: ["vacation wellness", "yoga", "meditation", "nature immersion", "mindfulness", "travel"]
  },
  {
    slug: "quick-glow-skincare-on-the-go-a-5-minute-travel-and-recovery-routine",
    categoryId: "radical-self-care",
    title: "Quick Glow Skincare on the Go: A 5-Minute Travel and Recovery Routine",
    excerpt: "A minimal, high-impact skincare routine for travel days, holidays, or after a long shift, hydrating, soothing, and de-puffing tired under-eyes in just 5 to 7 minutes.",
    date: "2026-08-07",
    readTime: "5 min read",
    category: "Wellness",
    image: "images/skincare-travel-kit.jpg",
    tags: ["skincare", "travel skincare", "quick routine", "eye care", "self-care habits"]
  },
  {
    slug: "top-5-affordable-travel-destinations-for-relaxation-no-visa-hassle",
    categoryId: "radical-self-care",
    title: "Top 5 Affordable Travel Destinations for Relaxation (No Visa Hassle)",
    excerpt: "True rest doesn't have to cost a fortune. Discover 5 affordable, visa-easy destinations perfect for slow, restorative travel on any budget.",
    date: "2026-08-06",
    readTime: "9 min read",
    category: "Wellness",
    image: "images/travel-destinations-collage.jpg",
    tags: ["budget travel", "affordable destinations", "visa-free travel", "slow travel", "travel tips"]
  },
  {
    slug: "slow-travel-for-the-overstimulated-woman-designing-trips-that-actually-restore-you",
    categoryId: "radical-self-care",
    title: "Slow Travel for the Overstimulated Woman: Designing Trips That Actually Restore You",
    excerpt: "A guide to choosing destinations, pacing, and daily rhythms that prioritize nervous-system calm, beauty, and quiet pleasure, think quiet coastal towns, thermal baths, and mornings with nowhere to be.",
    date: "2026-08-05",
    readTime: "7 min read",
    category: "Wellness",
    image: "images/slow-travel-coastal-town.jpg",
    tags: ["slow travel", "nervous system", "rest", "self-care", "overstimulation"]
  },
  {
    slug: "does-coffee-make-you-irritable-the-science-behind-caffeine-and-mood",
    categoryId: "radical-self-care",
    title: "Does Coffee Make You Irritable? The Science Behind Caffeine and Mood",
    excerpt: "That third cup might be doing more than waking you up. Here's why caffeine can quietly tip your calm into edge, and how to enjoy your ritual without the crash.",
    date: "2026-08-04",
    readTime: "4 min read",
    category: "Wellness",
    image: "images/coffee-mood.jpg",
    tags: ["caffeine", "coffee", "mood", "irritability", "self-care habits"]
  },
  {
    slug: "how-to-stop-comparing-your-glow-to-someone-elses",
    categoryId: "confidence-glow",
    title: "How to Stop Comparing Your Glow to Someone Else's",
    excerpt: "Comparison convinces you that someone else's glow is proof of what you're missing, when it's usually just proof of a different path entirely.",
    date: "2026-07-27",
    readTime: "6 min read",
    category: "Confidence & Glow",
    tags: ["confidence", "comparison", "self-worth", "inner glow"]
  },
  {
    slug: "the-quiet-kind-of-confidence-no-one-talks-about",
    categoryId: "confidence-glow",
    title: "The Quiet Kind of Confidence No One Talks About",
    excerpt: "The loudest confidence gets all the attention, but the kind that actually holds up under pressure is quieter, slower, and far less photogenic.",
    date: "2026-07-27",
    readTime: "6 min read",
    category: "Confidence & Glow",
    tags: ["confidence", "self-trust", "inner glow", "mindset"]
  },
  {
    slug: "how-to-feel-confident-before-you-feel-ready",
    categoryId: "confidence-glow",
    title: "How to Feel Confident Before You Feel Ready",
    excerpt: "Confidence rarely arrives before the moment that requires it, and waiting for that feeling is the very thing keeping you stuck in place.",
    date: "2026-07-27",
    readTime: "7 min read",
    category: "Confidence & Glow",
    tags: ["confidence", "mindset", "self-trust", "personal growth"]
  },
  {
    slug: "how-to-rest-without-guilt-when-you-were-raised-to-always-be-productive",
    categoryId: "radical-self-care",
    title: "How to Rest Without Guilt When You Were Raised to Always Be Productive",
    excerpt: "If rest feels like something you have to earn first, this is for the part of you that was taught your worth lives in your output, not your existence.",
    date: "2026-07-27",
    readTime: "7 min read",
    category: "Radical Self-Care",
    tags: ["rest", "guilt", "productivity culture", "burnout", "self-worth"]
  },
  {
    slug: "the-difference-between-self-care-and-self-soothing",
    categoryId: "radical-self-care",
    title: "The Difference Between Self-Care and Self-Soothing",
    excerpt: "One restores you and one just numbs you long enough to survive the day. Learning to tell them apart changes what you reach for when things get hard.",
    date: "2026-07-27",
    readTime: "6 min read",
    category: "Radical Self-Care",
    tags: ["self-soothing", "self-care", "emotional regulation", "coping habits", "nervous system"]
  },
  {
    slug: "what-radical-self-care-actually-means-and-why-it-is-not-selfish",
    categoryId: "radical-self-care",
    title: "What Radical Self-Care Actually Means (And Why It Is Not Selfish)",
    excerpt: "The word \"selfish\" was never really about you. It was a rule someone else needed you to follow, and it is time to look at where it came from.",
    date: "2026-07-27",
    readTime: "7 min read",
    category: "Radical Self-Care",
    tags: ["radical self-care", "boundaries", "self-worth", "emotional health", "mindset"]
  },
  {
    slug: "letting-go-of-relationships-that-no-longer-feel-safe-or-mutual",
    categoryId: "healing-boundaries",
    title: "Letting Go of Relationships That No Longer Feel Safe or Mutual",
    excerpt: "Some relationships don't end with a dramatic fight. They end quietly, the day you finally admit what the imbalance has been costing you all along.",
    date: "2026-07-27",
    readTime: "6 min read",
    category: "Healing & Boundaries",
    tags: ["relationships", "letting go", "boundaries", "healing", "self-worth"]
  },
  {
    slug: "how-to-respond-when-someone-does-not-respect-your-boundary",
    categoryId: "healing-boundaries",
    title: "How to Respond When Someone Does Not Respect Your Boundary",
    excerpt: "A boundary that gets tested isn't a failed boundary. It's the moment that actually determines whether it was real in the first place.",
    date: "2026-07-27",
    readTime: "6 min read",
    category: "Healing & Boundaries",
    tags: ["boundaries", "conflict", "self-respect", "relationships", "emotional health"]
  },
  {
    slug: "how-to-set-boundaries-without-feeling-cruel-or-selfish",
    categoryId: "healing-boundaries",
    title: "How to Set Boundaries Without Feeling Cruel or Selfish",
    excerpt: "A boundary is not a punishment you're handing someone. It's information about what you need to stay whole, and it's allowed to be simple.",
    date: "2026-07-27",
    readTime: "8 min read",
    category: "Healing & Boundaries",
    tags: ["boundaries", "self-respect", "healing", "emotional health", "guilt"]
  },
  {
    slug: "rebuilding-trust-in-yourself-after-a-painful-season",
    categoryId: "deep-self-love",
    title: "Rebuilding Trust in Yourself After a Painful Season",
    excerpt: "When a hard season leaves you doubting your own judgment, here is how to slowly, honestly rebuild trust with the person you have to live with forever: you.",
    date: "2026-07-27",
    readTime: "7 min read",
    category: "Deep Self-Love",
    tags: ["self-trust", "healing", "resilience", "self-love"]
  },
  {
    slug: "how-to-quiet-your-inner-critic-without-fighting-yourself",
    categoryId: "deep-self-love",
    title: "How to Quiet Your Inner Critic Without Fighting Yourself",
    excerpt: "You cannot silence the inner critic by arguing louder than it does. Here's a calmer, more effective way to change your relationship with that voice.",
    date: "2026-07-27",
    readTime: "6 min read",
    category: "Deep Self-Love",
    tags: ["inner critic", "self-love", "self-talk", "mental wellness"]
  },
  {
    slug: "the-difference-between-self-love-self-esteem-and-self-respect",
    categoryId: "deep-self-love",
    title: "The Difference Between Self-Love, Self-Esteem, and Self-Respect",
    excerpt: "These three words get used as if they're interchangeable, but they aren't, and knowing the difference changes which one you actually need to work on.",
    date: "2026-07-27",
    readTime: "6 min read",
    category: "Deep Self-Love",
    tags: ["self-love", "self-esteem", "self-respect", "personal growth"]
  },
  {
    slug: "creating-boundaries-and-dealing-with-anxiety-protecting-your-peace-in-your-glow-era",
    categoryId: "healing-boundaries",
    title: "Creating Boundaries and Dealing with Anxiety: Protecting Your Peace in Your Glow Era",
    excerpt: "Boundaries and anxiety are deeply intertwined. Here's how setting clear, compassionate limits creates the safety your nervous system craves.",
    date: "2026-07-27",
    readTime: "5 min read",
    category: "Mental Health",
    image: "images/boundaries-and-anxiety.png"
  },
  {
    slug: "how-alcohol-quietly-dims-your-glow",
    categoryId: "radical-self-care",
    title: "How Alcohol Quietly Dims Your Glow",
    excerpt: "It's not about never drinking again, it's about noticing what dims your light and choosing what helps you shine.",
    date: "2026-07-24",
    readTime: "3 min read",
    category: "Wellness",
    image: "images/drink.jpeg"
  },
  {
    slug: "the-skincare-in-a-can-ritual-how-sardines-became-the-secret-to-a-natural-glow",
    categoryId: "radical-self-care",
    title: "The Skincare in a Can Ritual: How Sardines Became the Secret to a Natural Glow",
    excerpt: "One humble tin of sardines, rich in omega-3s, vitamin D, and zinc, may be the simplest skin ritual in your Glow Era.",
    date: "2026-07-23",
    readTime: "3 min read",
    category: "Wellness Recipes",
    image: "images/sardine-skincare-ritual.jpeg"
  },
  {
    slug: "skincare-wellness-glow-from-the-inside-out-in-your-glow-era",
    categoryId: "radical-self-care",
    title: "Skincare Wellness: Glow From the Inside Out in Your Glow Era",
    excerpt: "Radiance isn't chased with trending products, it's cultivated through gentle topical care and deep inner nourishment.",
    date: "2026-07-21",
    readTime: "6 min read",
    category: "Wellness",
    image: "images/skincare-wellness-hero.jpeg"
  },
  {
    slug: "sleep-and-heart-health",
    categoryId: "radical-self-care",
    title: "Sleep and Heart Health: Why 7 to 9 Hours of Rest Is Your Heart's Best Ally",
    excerpt: "How sleep affects your heart, brain, and blood pressure, why the American Heart Association counts sleep as essential, and practical steps to sleep better tonight.",
    date: "2026-07-21",
    readTime: "7 min read",
    category: "Heart Health",
    image: "images/sleep.jpeg"
  },
  {
    slug: "glow-up-mornings-eating-breakfast-for-lasting-energy-focus-and-weight-control",
    categoryId: "radical-self-care",
    title: "Glow Up Mornings: Eating Breakfast for Lasting Energy, Focus and Weight Control",
    excerpt: "Why a protein-rich breakfast is the simple morning habit that transforms your energy, focus, and results, plus a make-ahead keto egg muffin recipe.",
    date: "2026-07-20",
    readTime: "5 min read",
    category: "Wellness Recipes",
    image: "images/breakfast.jpeg"
  },
  {
    slug: "self-care-day-at-home-gentle-pamper-routines-for-deep-relaxation-and-glow",
    categoryId: "radical-self-care",
    image: "images/self-care-pamper-day.jpeg",
    title: "Self-Care Day at Home: Gentle Pamper Routines for Deep Relaxation and Glow",
    excerpt: "A gentle at-home Soft Girl Pamper Day guide: cozy rituals, luxurious baths, body nourishment, and soul care for deep relaxation and natural glow.",
    date: "2026-07-20",
    readTime: "5 min read",
    category: "Self-Care"
  },
  {
    slug: "healing-childhood-wounds-and-trauma-a-path-to-wholeness",
    categoryId: "healing-boundaries",
    image: "images/healing-childhood-wounds.jpeg",
    title: "Healing Childhood Wounds and Trauma: A Path to Wholeness",
    excerpt: "Childhood wounds shape us, but they don't have to define us. A gentle, evidence-based guide to healing your inner child and reclaiming wholeness.",
    date: "2026-07-18",
    readTime: "4 min read",
    category: "Mental Health"
  },
  {
    slug: "7-factors-that-worsen-mental-health-as-you-age-and-gentle-ways-to-protect-it",
    categoryId: "healing-boundaries",
    title: "7 Factors That Worsen Mental Health As You Age (And Gentle Ways to Protect It)",
    excerpt: "Understanding the common factors behind mental health decline as you age, plus gentle, realistic ways to protect your peace.",
    date: "2026-07-17",
    readTime: "3 min read",
    category: "Mental Health",
    image: "images/mental-health-aging.jpeg"
  },
  {
    slug: "am-i-anxious-or-just-stressed-understanding-the-difference-and-how-to-find-your-calm",
    categoryId: "healing-boundaries",
    title: "Am I Anxious or Just Stressed? Understanding the Difference and How to Find Your Calm",
    excerpt: "How to tell stress and anxiety apart, the symptoms of each, self-reflection questions, and gentle ways to find your calm.",
    date: "2026-07-17",
    readTime: "4 min read",
    category: "Wellness",
    image: "images/anxious-or-just-stressed.png"
  },
  {
    slug: "home-pilates-for-men-and-women-complete-beginner-guide",
    categoryId: "radical-self-care",
    title: "Home Pilates for Men and Women: Complete Beginner Guide",
    excerpt: "A complete beginner guide to building core strength, posture, and flexibility with a simple 20-minute home Pilates routine for men and women.",
    date: "2026-07-16",
    readTime: "3 min read",
    category: "Fitness",
    image: "images/home-pilates.jpeg"
  },
  {
    slug: "easy-one-pan-keto-chicken-and-vegetables-low-carb-20-minutes",
    categoryId: "radical-self-care",
    title: "Easy One-Pan Keto Chicken and Vegetables (Low Carb, 20 Minutes)",
    excerpt: "A 20-minute, one-pan keto chicken and vegetable dinner that is high in protein, low in carbs, and easy to meal prep.",
    date: "2026-07-14",
    readTime: "2 min read",
    category: "Wellness Recipes",
    image: "images/keto-chicken-veggies.jpeg"
  },
  {
    slug: "morning-glow-magic-detox-tea-lemon-and-lime-recipe-for-glowing-skin-and-energy",
    categoryId: "radical-self-care",
    title: "Morning Glow Magic Detox Tea: Lemon and Lime Recipe for Glowing Skin and Energy",
    excerpt: "A caffeine-light citrus detox tea with ginger, turmeric, and hibiscus for glowing skin, gut health, and natural morning energy.",
    date: "2026-07-13",
    readTime: "2 min read",
    category: "Wellness Recipes",
    image: "images/morning-glow-detox-tea.jpeg"
  },
  {
    slug: "the-ritual-reclaiming-joy-after-burnout",
    categoryId: "healing-boundaries",
    title: "The Ritual: Reclaiming Joy After Burnout",
    excerpt: "A gentle 40-minute evening wind-down ritual, stretching, chamomile tea, and gratitude, to release workday tension and reclaim your rest.",
    date: "2026-07-11",
    readTime: "2 min read",
    category: "Wellness",
    image: "images/evening-wind-down-ritual.jpeg"
  },
  {
    slug: "reclaiming-joy-after-burnout-a-gentle-guide-to-feeling-like-yourself-again",
    categoryId: "healing-boundaries",
    title: "Reclaiming Joy After Burnout: A Gentle Guide to Feeling Like Yourself Again",
    excerpt: "Burnout quietly steals your joy, here is how to slowly rebuild rest, pleasure, and meaning without forcing it.",
    date: "2026-07-10",
    readTime: "6 min read",
    category: "Wellness",
    image: "images/reclaiming-joy-after-burnout.png"
  },
  {
    slug: "how-to-build-unshakable-confidence-one-kept-promise-at-a-time",
    categoryId: "confidence-glow",
    title: "How to Build Unshakable Confidence (One Kept Promise at a Time)",
    excerpt: "Confidence is not something you are born with. It is built quietly, in private, one small kept promise at a time. Here is how to begin.",
    date: "2026-07-09",
    readTime: "5 min read",
    category: "Confidence",
    image: "images/unshakable-confidence.jpg"
  },
  {
    slug: "why-putting-yourself-last-feels-normal-but-is-quietly-destroying-your-glow",
    categoryId: "deep-self-love",
    title: "Why Putting Yourself Last Feels Normal (But Is Quietly Destroying Your Glow)",
    excerpt: "Choosing everyone else first feels like the default setting. Here are 5 gentle ways to start choosing you, without the guilt.",
    date: "2026-07-08",
    readTime: "4 min read",
    category: "Self-Care",
    image: "images/putting-yourself-last.png"
  },
  {
    slug: "nutrition-without-the-guilt-how-to-eat-in-your-glow-era",
    categoryId: "radical-self-care",
    title: "Nutrition Without the Guilt: How to Eat in Your Glow Era",
    excerpt: "Diet culture taught you to fear food. Here's a gentler, more sustainable way to nourish your body and actually feel good.",
    date: "2026-07-07",
    readTime: "3 min read",
    category: "Wellness",
    image: "images/nutrition.jpeg"
  },
  {
    slug: "the-silent-killer-how-lack-of-sleep-raises-your-risk-of-stroke",
    categoryId: "radical-self-care",
    title: "The Silent Killer: How Lack of Sleep Raises Your Risk of Stroke",
    excerpt: "How chronic sleep loss quietly raises your risk of stroke, heart disease, and more, plus practical tips to sleep better tonight.",
    date: "2026-07-06",
    readTime: "3 min read",
    category: "Wellness",
    image: "images/glow-arrow-one.png"
  },
  {
    slug: "why-your-self-care-routine-keeps-failing",
    categoryId: "radical-self-care",
    title: "Why Your Self-Care Routine Keeps Failing (And What Actually Works)",
    excerpt: "Most self-care advice is built for a life you don't have. Here's the gentler, more honest approach Glow Era teaches instead.",
    date: "2026-07-06",
    readTime: "5 min read",
    category: "Self-Care"
  },
  {
    slug: "the-boundary-you-are-most-afraid-to-set",
    categoryId: "healing-boundaries",
    title: "The Boundary You're Most Afraid to Set (And Why It Will Set You Free)",
    excerpt: "Boundaries aren't walls. They're the quiet, powerful act of telling the truth about what you need.",
    date: "2026-07-05",
    readTime: "4 min read",
    category: "Boundaries"
  },
  {
    slug: "how-to-start-your-glow-era-today",
    categoryId: "confidence-glow",
    title: "How to Start Your Glow Era Today (Even If You Don't Feel Ready)",
    excerpt: "You don't need a clean slate, a new year, or perfect timing. You just need to begin. Here's how.",
    date: "2026-07-04",
    readTime: "4 min read",
    category: "Confidence"
  }

];
