class BusinessInsights:
    """Generate automated business insights"""
    
    @staticmethod
    def analyze_retention(day1_retention, industry_benchmark=40):
        """Analyze retention performance"""
        insights = []
        
        if day1_retention < industry_benchmark * 0.8:
            insights.append({
                'type': 'critical',
                'title': 'Critical: Low Day 1 Retention',
                'description': f'Current Day 1 retention ({day1_retention:.1f}%) is significantly below industry benchmark ({industry_benchmark}%)',
                'recommendations': [
                    'Implement enhanced onboarding with mandatory micro-lessons',
                    'Add progress indicators and early success celebrations',
                    'Personalize learning paths based on user goals'
                ],
                'impact': '+35% retention improvement could increase MRR by $75K-120K'
            })
        elif day1_retention < industry_benchmark:
            insights.append({
                'type': 'warning',
                'title': 'Opportunity: Retention Improvement',
                'description': f'Day 1 retention ({day1_retention:.1f}%) is below industry benchmark',
                'recommendations': [
                    'A/B test different onboarding flows',
                    'Analyze drop-off points in user journey',
                    'Implement push notification campaigns'
                ],
                'impact': '+15% retention improvement worth $30K+ monthly'
            })
        else:
            insights.append({
                'type': 'success',
                'title': 'Strength: Strong Retention',
                'description': f'Day 1 retention ({day1_retention:.1f}%) exceeds industry benchmark',
                'recommendations': [
                    'Focus on long-term retention (Day 7, Day 30)',
                    'Leverage high retention for referral programs',
                    'Scale successful onboarding practices'
                ],
                'impact': 'Maintain competitive advantage'
            })
        
        return insights
    
    @staticmethod
    def analyze_conversion(conversion_rate, target_rate=25):
        """Analyze conversion performance"""
        insights = []
        
        if conversion_rate < target_rate * 0.8:
            insights.append({
                'type': 'warning',
                'title': 'Opportunity: Conversion Optimization',
                'description': f'Premium conversion ({conversion_rate:.1f}%) has significant room for improvement',
                'recommendations': [
                    'Add achievement-based premium triggers',
                    'Implement 7-day free trial offer',
                    'Create premium feature demonstrations',
                    'Add social proof elements'
                ],
                'impact': '+30% conversion improvement worth $50K+ monthly'
            })
        elif conversion_rate < target_rate:
            insights.append({
                'type': 'info',
                'title': 'Growth: Conversion Enhancement',
                'description': f'Conversion rate ({conversion_rate:.1f}%) can be improved',
                'recommendations': [
                    'A/B test different pricing strategies',
                    'Optimize premium value proposition',
                    'Implement usage-based upgrade prompts'
                ],
                'impact': '+15% conversion improvement worth $25K+ monthly'
            })
        else:
            insights.append({
                'type': 'success',
                'title': 'Excellence: Strong Conversion',
                'description': f'Premium conversion ({conversion_rate:.1f}%) exceeds target',
                'recommendations': [
                    'Focus on premium user retention',
                    'Expand premium feature set',
                    'Implement referral rewards for premium users'
                ],
                'impact': 'Maximize premium user lifetime value'
            })
        
        return insights
    
    @staticmethod
    def analyze_engagement(avg_session_time, completion_rate):
        """Analyze user engagement metrics"""
        insights = []
        
        if avg_session_time > 120 and completion_rate > 75:
            insights.append({
                'type': 'success',
                'title': 'Excellence: High User Engagement',
                'description': f'Strong engagement metrics (Session: {avg_session_time:.1f}min, Completion: {completion_rate:.1f}%)',
                'recommendations': [
                    'Leverage engagement for premium conversion',
                    'Create advanced learning paths',
                    'Implement user-generated content features'
                ],
                'impact': 'Strong product-market fit foundation'
            })
        elif avg_session_time > 90:
            insights.append({
                'type': 'info',
                'title': 'Strength: Good Engagement',
                'description': f'Solid engagement levels indicate content quality',
                'recommendations': [
                    'Optimize lesson pacing and structure',
                    'Add interactive elements to lessons',
                    'Implement progress tracking features'
                ],
                'impact': 'Foundation for retention improvements'
            })
        else:
            insights.append({
                'type': 'warning',
                'title': 'Concern: Low Engagement',
                'description': f'Engagement metrics suggest content or UX issues',
                'recommendations': [
                    'Audit content quality and relevance',
                    'Simplify user interface',
                    'Add gamification elements',
                    'Implement personalized content recommendations'
                ],
                'impact': 'Critical for retention and conversion improvement'
            })
        
        return insights