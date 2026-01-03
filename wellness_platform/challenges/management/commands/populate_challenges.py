from django.core.management.base import BaseCommand
from django.utils.text import slugify
from challenges.models import Challenge


class Command(BaseCommand):
    help = 'Populate the database with 30 diverse fitness challenges'

    def handle(self, *args, **options):
        challenges_data = [
            {
                'title': '10,000 Steps Daily Challenge',
                'description': 'Transform your health with the power of walking! This 30-day challenge will help you build a sustainable habit of walking 10,000 steps every day. Perfect for beginners and those looking to increase their daily activity level.',
                'short_description': 'Walk 10,000 steps every day for 30 days and build a healthy habit',
                'duration_days': 30,
                'difficulty': 'beginner',
                'goal_type': 'fitness',
                'tracking_type': 'numeric',
                'daily_target': 10000,
                'daily_requirement': 'Walk 10,000 steps (about 5 miles)',
                'points_reward': 150,
                'badge_name': 'Step Master',
                'badge_icon': '🚶‍♀️',
                'is_featured': True
            },
            {
                'title': '30-Day Push-Up Challenge',
                'description': 'Build upper body strength progressively with this structured push-up program. Starting with basic push-ups and advancing to more challenging variations, this challenge is perfect for building chest, shoulder, and arm strength.',
                'short_description': 'Progressive push-up program to build upper body strength',
                'duration_days': 30,
                'difficulty': 'intermediate',
                'goal_type': 'fitness',
                'tracking_type': 'count',
                'daily_target': 20,
                'daily_requirement': 'Complete daily push-up routine (starts at 5, builds to 50)',
                'points_reward': 200,
                'badge_name': 'Push-Up Pro',
                'badge_icon': '💪',
                'is_featured': False
            },
            {
                'title': 'Hydration Hero Challenge',
                'description': 'Stay properly hydrated for optimal health and energy! This challenge focuses on drinking adequate water throughout the day. Learn to listen to your body and maintain proper hydration levels.',
                'short_description': 'Drink 8 glasses of water daily to stay properly hydrated',
                'duration_days': 21,
                'difficulty': 'beginner',
                'goal_type': 'hydration',
                'tracking_type': 'count',
                'daily_target': 8,
                'daily_requirement': 'Drink 8 glasses (64oz) of water',
                'points_reward': 120,
                'badge_name': 'Hydration Hero',
                'badge_icon': '💧',
                'is_featured': True
            },
            {
                'title': '5K Running Preparation',
                'description': 'Train systematically to run your first 5K! This comprehensive program takes you from couch to 5K with a proven training plan that gradually builds your endurance and speed.',
                'short_description': 'Progressive training program to complete your first 5K run',
                'duration_days': 42,
                'difficulty': 'intermediate',
                'goal_type': 'endurance',
                'tracking_type': 'time',
                'daily_target': 30,
                'daily_requirement': 'Follow daily run/walk training schedule (30-45 minutes)',
                'points_reward': 300,
                'badge_name': '5K Finisher',
                'badge_icon': '🏃‍♂️',
                'is_featured': True
            },
            {
                'title': 'Daily Meditation Journey',
                'description': 'Discover inner peace and mental clarity through daily meditation practice. This gentle introduction to mindfulness will help reduce stress, improve focus, and enhance overall well-being.',
                'short_description': 'Practice mindfulness meditation for 15 minutes daily',
                'duration_days': 28,
                'difficulty': 'beginner',
                'goal_type': 'mental_health',
                'tracking_type': 'time',
                'daily_target': 15,
                'daily_requirement': 'Meditate for 15 minutes using guided meditation',
                'points_reward': 180,
                'badge_name': 'Zen Master',
                'badge_icon': '🧘‍♀️',
                'is_featured': False
            },
            {
                'title': 'Flexibility & Stretching',
                'description': 'Improve your flexibility and reduce muscle tension with daily stretching routines. Perfect for office workers, athletes, or anyone looking to increase mobility and prevent injuries.',
                'short_description': 'Daily 20-minute stretching routine for better flexibility',
                'duration_days': 21,
                'difficulty': 'beginner',
                'goal_type': 'flexibility',
                'tracking_type': 'time',
                'daily_target': 20,
                'daily_requirement': 'Complete 20-minute full-body stretching routine',
                'points_reward': 140,
                'badge_name': 'Flexibility Champion',
                'badge_icon': '🤸‍♀️',
                'is_featured': False
            },
            {
                'title': 'Bodyweight Strength Circuit',
                'description': 'Build functional strength using only your body weight! This challenging program includes squats, lunges, planks, and more to create a complete strength training routine.',
                'short_description': 'Complete bodyweight exercises to build total body strength',
                'duration_days': 35,
                'difficulty': 'intermediate',
                'goal_type': 'fitness',
                'tracking_type': 'boolean',
                'daily_target': None,
                'daily_requirement': 'Complete 30-minute bodyweight circuit training',
                'points_reward': 220,
                'badge_name': 'Bodyweight Beast',
                'badge_icon': '🏋️‍♂️',
                'is_featured': False
            },
            {
                'title': 'Healthy Sleep Schedule',
                'description': 'Optimize your sleep for better health and performance. This challenge helps you establish a consistent sleep schedule and improve sleep quality through proven sleep hygiene practices.',
                'short_description': 'Maintain 7-8 hours of quality sleep nightly',
                'duration_days': 21,
                'difficulty': 'beginner',
                'goal_type': 'sleep',
                'tracking_type': 'time',
                'daily_target': 8,
                'daily_requirement': 'Sleep 7-8 hours per night with consistent bedtime',
                'points_reward': 160,
                'badge_name': 'Sleep Champion',
                'badge_icon': '😴',
                'is_featured': False
            },
            {
                'title': 'Plant-Based Nutrition',
                'description': 'Explore the benefits of plant-based eating! Incorporate more fruits, vegetables, and whole foods into your diet while learning delicious, nutritious recipes.',
                'short_description': 'Eat 5+ servings of fruits and vegetables daily',
                'duration_days': 30,
                'difficulty': 'beginner',
                'goal_type': 'nutrition',
                'tracking_type': 'count',
                'daily_target': 5,
                'daily_requirement': 'Consume at least 5 servings of fruits and vegetables',
                'points_reward': 200,
                'badge_name': 'Plant Powered',
                'badge_icon': '🥗',
                'is_featured': True
            },
            {
                'title': 'Advanced HIIT Training',
                'description': 'Take your fitness to the next level with High-Intensity Interval Training! This challenging program maximizes fat burn and cardiovascular fitness in minimal time.',
                'short_description': 'High-intensity interval training for maximum results',
                'duration_days': 28,
                'difficulty': 'advanced',
                'goal_type': 'fitness',
                'tracking_type': 'time',
                'daily_target': 25,
                'daily_requirement': 'Complete 25-minute HIIT workout with maximum effort',
                'points_reward': 250,
                'badge_name': 'HIIT Hero',
                'badge_icon': '⚡',
                'is_featured': False
            },
            {
                'title': 'Gratitude & Mindfulness',
                'description': 'Cultivate a positive mindset through daily gratitude practice. Write down three things you\'re grateful for each day and watch your perspective transform.',
                'short_description': 'Practice daily gratitude journaling for mental wellness',
                'duration_days': 30,
                'difficulty': 'beginner',
                'goal_type': 'mental_health',
                'tracking_type': 'boolean',
                'daily_target': None,
                'daily_requirement': 'Write 3 things you\'re grateful for in your journal',
                'points_reward': 150,
                'badge_name': 'Gratitude Guru',
                'badge_icon': '🙏',
                'is_featured': False
            },
            {
                'title': 'Core Strength Builder',
                'description': 'Develop a strong, stable core with targeted exercises. This program focuses on planks, crunches, and functional core movements for better posture and strength.',
                'short_description': 'Build core strength with daily targeted exercises',
                'duration_days': 21,
                'difficulty': 'intermediate',
                'goal_type': 'fitness',
                'tracking_type': 'time',
                'daily_target': 15,
                'daily_requirement': 'Complete 15-minute core strengthening routine',
                'points_reward': 170,
                'badge_name': 'Core Crusher',
                'badge_icon': '🎯',
                'is_featured': False
            },
            {
                'title': 'Sugar-Free Challenge',
                'description': 'Break free from sugar addiction and discover natural energy! This challenge eliminates added sugars while teaching you to enjoy naturally sweet foods.',
                'short_description': 'Eliminate added sugars and processed sweets for 14 days',
                'duration_days': 14,
                'difficulty': 'intermediate',
                'goal_type': 'nutrition',
                'tracking_type': 'boolean',
                'daily_target': None,
                'daily_requirement': 'Avoid all added sugars and processed sweet foods',
                'points_reward': 180,
                'badge_name': 'Sugar Slayer',
                'badge_icon': '🚫🍭',
                'is_featured': True
            },
            {
                'title': 'Morning Yoga Flow',
                'description': 'Start each day with energizing yoga practice. This gentle morning routine improves flexibility, balance, and mental clarity while setting a positive tone for the day.',
                'short_description': 'Begin each day with 20 minutes of energizing yoga',
                'duration_days': 30,
                'difficulty': 'beginner',
                'goal_type': 'flexibility',
                'tracking_type': 'time',
                'daily_target': 20,
                'daily_requirement': 'Complete 20-minute morning yoga flow',
                'points_reward': 190,
                'badge_name': 'Morning Yogi',
                'badge_icon': '🧘‍♂️',
                'is_featured': False
            },
            {
                'title': 'Marathon Training Program',
                'description': 'Train for the ultimate running achievement! This comprehensive 16-week program prepares you for a full 26.2-mile marathon with structured training phases.',
                'short_description': 'Comprehensive 16-week marathon training program',
                'duration_days': 112,
                'difficulty': 'expert',
                'goal_type': 'endurance',
                'tracking_type': 'time',
                'daily_target': 60,
                'daily_requirement': 'Follow structured running plan (varies by day: easy runs, tempo, long runs)',
                'points_reward': 500,
                'badge_name': 'Marathon Finisher',
                'badge_icon': '🏃‍♀️',
                'is_featured': True
            },
            {
                'title': 'Digital Detox Challenge',
                'description': 'Reconnect with the real world by reducing screen time and social media usage. This challenge helps you find balance in our digital age.',
                'short_description': 'Limit recreational screen time to 2 hours daily',
                'duration_days': 14,
                'difficulty': 'intermediate',
                'goal_type': 'mental_health',
                'tracking_type': 'time',
                'daily_target': 2,
                'daily_requirement': 'Limit recreational screen time to 2 hours maximum',
                'points_reward': 140,
                'badge_name': 'Digital Detoxer',
                'badge_icon': '📱❌',
                'is_featured': False
            },
            {
                'title': 'Plank Power Challenge',
                'description': 'Build incredible core strength and endurance with progressive plank holds. Start with 30 seconds and work your way up to holding a plank for 5 minutes!',
                'short_description': 'Progressive plank challenge building to 5-minute holds',
                'duration_days': 30,
                'difficulty': 'intermediate',
                'goal_type': 'fitness',
                'tracking_type': 'time',
                'daily_target': 60,
                'daily_requirement': 'Hold plank position for prescribed daily duration',
                'points_reward': 200,
                'badge_name': 'Plank Master',
                'badge_icon': '🏋️‍♀️',
                'is_featured': False
            },
            {
                'title': 'Intermittent Fasting 16:8',
                'description': 'Discover the benefits of intermittent fasting with the popular 16:8 method. Fast for 16 hours and eat within an 8-hour window to optimize metabolism and energy.',
                'short_description': 'Practice 16:8 intermittent fasting for metabolic health',
                'duration_days': 21,
                'difficulty': 'intermediate',
                'goal_type': 'nutrition',
                'tracking_type': 'boolean',
                'daily_target': None,
                'daily_requirement': 'Fast for 16 hours, eat within 8-hour window',
                'points_reward': 180,
                'badge_name': 'Fasting Pro',
                'badge_icon': '⏰',
                'is_featured': False
            },
            {
                'title': 'Cold Shower Therapy',
                'description': 'Build mental toughness and boost immunity with daily cold showers. This challenging practice improves circulation, mood, and stress resilience.',
                'short_description': 'Take daily cold showers to build resilience and health',
                'duration_days': 21,
                'difficulty': 'advanced',
                'goal_type': 'mental_health',
                'tracking_type': 'time',
                'daily_target': 2,
                'daily_requirement': 'Take 2-minute cold shower (below 60°F)',
                'points_reward': 210,
                'badge_name': 'Cold Warrior',
                'badge_icon': '🥶',
                'is_featured': False
            },
            {
                'title': 'Strength Training Basics',
                'description': 'Learn proper strength training fundamentals with bodyweight and basic equipment. Perfect for beginners wanting to build muscle and bone density safely.',
                'short_description': 'Master basic strength training movements and form',
                'duration_days': 28,
                'difficulty': 'beginner',
                'goal_type': 'fitness',
                'tracking_type': 'boolean',
                'daily_target': None,
                'daily_requirement': 'Complete 3 strength training sessions per week (45 minutes each)',
                'points_reward': 220,
                'badge_name': 'Strength Starter',
                'badge_icon': '🏋️',
                'is_featured': False
            },
            {
                'title': '10-Minute Daily Meditation',
                'description': 'Build a sustainable meditation practice with just 10 minutes per day. Learn different meditation techniques and experience the benefits of mindfulness.',
                'short_description': 'Establish consistent 10-minute daily meditation practice',
                'duration_days': 21,
                'difficulty': 'beginner',
                'goal_type': 'mindfulness',
                'tracking_type': 'time',
                'daily_target': 10,
                'daily_requirement': 'Meditate for 10 minutes using any technique',
                'points_reward': 130,
                'badge_name': 'Mindful Meditator',
                'badge_icon': '🕉️',
                'is_featured': False
            },
            {
                'title': 'Healthy Meal Prep Sunday',
                'description': 'Master the art of meal preparation for the week ahead. Learn to plan, shop, and prepare nutritious meals that support your health goals.',
                'short_description': 'Prepare healthy meals every Sunday for the week',
                'duration_days': 28,
                'difficulty': 'beginner',
                'goal_type': 'nutrition',
                'tracking_type': 'boolean',
                'daily_target': None,
                'daily_requirement': 'Prep healthy meals every Sunday for the upcoming week',
                'points_reward': 160,
                'badge_name': 'Meal Prep Master',
                'badge_icon': '🥘',
                'is_featured': False
            },
            {
                'title': 'Swimming Endurance Challenge',
                'description': 'Improve cardiovascular fitness and full-body strength through swimming. Perfect low-impact exercise for building endurance and technique.',
                'short_description': 'Swim laps for 30 minutes, 4 times per week',
                'duration_days': 28,
                'difficulty': 'intermediate',
                'goal_type': 'endurance',
                'tracking_type': 'time',
                'daily_target': 30,
                'daily_requirement': 'Swim continuously for 30 minutes (4 sessions per week)',
                'points_reward': 240,
                'badge_name': 'Swimming Strong',
                'badge_icon': '🏊‍♀️',
                'is_featured': False
            },
            {
                'title': 'Stair Climbing Power',
                'description': 'Transform any staircase into your gym! This high-intensity challenge builds leg strength, cardiovascular fitness, and functional movement patterns.',
                'short_description': 'Climb stairs for cardio and leg strengthening',
                'duration_days': 21,
                'difficulty': 'intermediate',
                'goal_type': 'fitness',
                'tracking_type': 'count',
                'daily_target': 10,
                'daily_requirement': 'Climb 10 flights of stairs (up and down counts as 2)',
                'points_reward': 170,
                'badge_name': 'Stair Master',
                'badge_icon': '🪜',
                'is_featured': False
            },
            {
                'title': 'Posture Perfect Challenge',
                'description': 'Improve your posture through targeted exercises and awareness. Combat the effects of desk work and technology use with daily posture practice.',
                'short_description': 'Perform daily posture exercises and awareness checks',
                'duration_days': 21,
                'difficulty': 'beginner',
                'goal_type': 'general',
                'tracking_type': 'boolean',
                'daily_target': None,
                'daily_requirement': 'Complete posture exercises and hourly posture checks',
                'points_reward': 140,
                'badge_name': 'Posture Pro',
                'badge_icon': '🕴️',
                'is_featured': False
            },
            {
                'title': 'Weekend Warrior Workouts',
                'description': 'Maximize your fitness with intensive weekend training sessions. Perfect for busy professionals who want to maintain fitness with limited time.',
                'short_description': 'Complete intensive weekend workouts (Saturday & Sunday)',
                'duration_days': 28,
                'difficulty': 'advanced',
                'goal_type': 'fitness',
                'tracking_type': 'boolean',
                'daily_target': None,
                'daily_requirement': 'Complete 90-minute intensive workout each weekend day',
                'points_reward': 280,
                'badge_name': 'Weekend Warrior',
                'badge_icon': '⚔️',
                'is_featured': False
            },
            {
                'title': 'Nature Walking Challenge',
                'description': 'Connect with nature while improving your fitness. Take your walking routine outdoors to parks, trails, and natural settings for mental and physical benefits.',
                'short_description': 'Walk in nature for 45 minutes, 5 days per week',
                'duration_days': 30,
                'difficulty': 'beginner',
                'goal_type': 'general',
                'tracking_type': 'time',
                'daily_target': 45,
                'daily_requirement': 'Walk in natural settings for 45 minutes (5 days per week)',
                'points_reward': 190,
                'badge_name': 'Nature Walker',
                'badge_icon': '🌲',
                'is_featured': True
            },
            {
                'title': 'Balance & Stability Training',
                'description': 'Improve your balance, proprioception, and injury prevention with targeted stability exercises. Essential for aging gracefully and athletic performance.',
                'short_description': 'Daily balance and stability exercises for injury prevention',
                'duration_days': 21,
                'difficulty': 'beginner',
                'goal_type': 'general',
                'tracking_type': 'time',
                'daily_target': 15,
                'daily_requirement': 'Complete 15-minute balance and stability routine',
                'points_reward': 150,
                'badge_name': 'Balance Master',
                'badge_icon': '⚖️',
                'is_featured': False
            },
            {
                'title': 'Burpee Blast Challenge',
                'description': 'Master the ultimate full-body exercise! Progress from 5 to 100 burpees over 30 days. This intense challenge builds strength, endurance, and mental toughness.',
                'short_description': 'Progressive burpee challenge building to 100 daily',
                'duration_days': 30,
                'difficulty': 'advanced',
                'goal_type': 'fitness',
                'tracking_type': 'count',
                'daily_target': 50,
                'daily_requirement': 'Complete daily burpee target (progresses from 5 to 100)',
                'points_reward': 300,
                'badge_name': 'Burpee Beast',
                'badge_icon': '🔥',
                'is_featured': True
            },
            {
                'title': 'Mindful Eating Practice',
                'description': 'Transform your relationship with food through mindful eating practices. Learn to eat slowly, appreciate flavors, and recognize hunger/fullness cues.',
                'short_description': 'Practice mindful eating at every meal',
                'duration_days': 21,
                'difficulty': 'beginner',
                'goal_type': 'mindfulness',
                'tracking_type': 'boolean',
                'daily_target': None,
                'daily_requirement': 'Eat at least one meal mindfully (no distractions, slow eating)',
                'points_reward': 140,
                'badge_name': 'Mindful Eater',
                'badge_icon': '🍽️',
                'is_featured': False
            }
        ]

        created_count = 0
        for challenge_data in challenges_data:
            slug = slugify(challenge_data['title'])
            
            # Check if challenge already exists
            if Challenge.objects.filter(slug=slug).exists():
                self.stdout.write(
                    self.style.WARNING(f'Challenge "{challenge_data["title"]}" already exists. Skipping.')
                )
                continue

            # Create the challenge
            challenge = Challenge.objects.create(
                title=challenge_data['title'],
                slug=slug,
                description=challenge_data['description'],
                short_description=challenge_data['short_description'],
                duration_days=challenge_data['duration_days'],
                difficulty=challenge_data['difficulty'],
                goal_type=challenge_data['goal_type'],
                tracking_type=challenge_data['tracking_type'],
                daily_target=challenge_data.get('daily_target'),
                daily_requirement=challenge_data['daily_requirement'],
                points_reward=challenge_data['points_reward'],
                badge_name=challenge_data['badge_name'],
                badge_icon=challenge_data['badge_icon'],
                is_active=True,
                is_featured=challenge_data.get('is_featured', False)
            )
            
            created_count += 1
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created challenge: "{challenge.title}"')
            )

        self.stdout.write(
            self.style.SUCCESS(f'\nTotal challenges created: {created_count}')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Total challenges in database: {Challenge.objects.count()}')
        )