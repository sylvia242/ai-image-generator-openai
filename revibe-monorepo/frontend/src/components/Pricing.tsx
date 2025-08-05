import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Check } from "lucide-react";

export const Pricing = () => {
  const plans = [
    {
      name: "Free",
      price: "Free",
      period: "forever",
      description: "Try one room transformation daily",
      features: [
        "1 room per day",
        "3 design styles",
        "Shoppable product list",
        "Standard support",
        "No credit card required"
      ],
      popular: false
    },
    {
      name: "Starter", 
      price: "$19",
      period: "one-time",
      description: "Perfect for small makeovers",
      features: [
        "Up to 50 images",
        "Unlimited style options",
        "Advanced shopping integration",
        "Priority support",
        "Download high-res images",
        "30-day access"
      ],
      popular: true
    },
    {
      name: "Pro",
      price: "$49",
      period: "one-time",
      description: "For complete home transformations",
      features: [
        "Up to 200 images",
        "Unlimited style options",
        "Advanced shopping integration",
        "Priority support", 
        "Download high-res images",
        "90-day access",
        "Bulk processing"
      ],
      popular: false
    }
  ];

  return (
    <section id="pricing" className="py-20 px-4 bg-background">
      <div className="container mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-foreground mb-4">
            Simple, Transparent Pricing
          </h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Choose the plan that fits your needs. All plans include our AI design engine 
            and shoppable product recommendations.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          {plans.map((plan, index) => (
            <Card 
              key={index} 
              className={`relative shadow-elegant transition-all duration-300 hover:shadow-glow ${
                plan.popular ? 'border-primary shadow-glow scale-105' : ''
              }`}
            >
              {plan.popular && (
                <Badge className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                  Most Popular
                </Badge>
              )}
              
              <CardHeader className="text-center pb-8">
                <CardTitle className="text-2xl font-bold">{plan.name}</CardTitle>
                <div className="mt-4">
                  <span className="text-4xl font-bold text-primary">{plan.price}</span>
                  <span className="text-muted-foreground ml-2">{plan.period}</span>
                </div>
                <p className="text-muted-foreground mt-2">{plan.description}</p>
              </CardHeader>

              <CardContent className="space-y-6">
                <ul className="space-y-3">
                  {plan.features.map((feature, idx) => (
                    <li key={idx} className="flex items-center">
                      <Check className="h-5 w-5 text-secondary mr-3 flex-shrink-0" />
                      <span className="text-sm">{feature}</span>
                    </li>
                  ))}
                </ul>

                <Button 
                  className={`w-full ${plan.popular ? 'shadow-glow' : ''}`}
                  variant={plan.popular ? 'default' : 'outline'}
                  size="lg"
                >
                  {plan.popular ? 'Start Free Trial' : 'Get Started'}
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>

        <div className="text-center mt-12">
          <p className="text-muted-foreground mb-4">
            All plans include a 7-day money-back guarantee
          </p>
          <div className="flex flex-wrap justify-center gap-8 text-sm text-muted-foreground">
            <span>✓ No setup fees</span>
            <span>✓ Cancel anytime</span>
            <span>✓ 24/7 support</span>
            <span>✓ Free design consultations</span>
          </div>
        </div>
      </div>
    </section>
  );
};