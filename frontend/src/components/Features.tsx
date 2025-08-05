import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export const Features = () => {
  const features = [
    {
      title: "AI-Powered Transformations",
      description: "Upload room photos and get stunning design alternatives with complete shopping lists for easy implementation.",
      icon: "🤖",
      benefits: ["Instant results", "Multiple style options", "Implementation ready"]
    },
    {
      title: "Complete Shopping Integration",
      description: "Bridge the gap between inspiration and reality. Every design element comes with direct purchase links and pricing.",
      icon: "🛍️",
      benefits: ["Ready to buy", "Real pricing", "Trusted retailers"]
    },
    {
      title: "Style-Focused Recommendations",
      description: "Designs prioritize your personal aesthetic with high-impact, budget-conscious changes.",
      icon: "🎨",
      benefits: ["Budget optimization", "Style consistency", "Personal preferences"]
    },
    {
      title: "Room Optimization",
      description: "Specifically designed for real living spaces with durable, beautiful, and functional selections.",
      icon: "🏠",
      benefits: ["Livable designs", "Photo-worthy spaces", "Easy maintenance"]
    },
    {
      title: "From Design to Reality",
      description: "Skip the guesswork. Get detailed implementation guides with product lists that turn inspiration into your actual space.",
      icon: "✨",
      benefits: ["Step-by-step guides", "Real transformation", "No design experience needed"]
    },
    {
      title: "Complete Style Guides",
      description: "Get detailed room concepts with mood descriptions perfect for listing photos and guest communication.",
      icon: "📝",
      benefits: ["Marketing copy", "Style narratives", "Guest appeal"]
    }
  ];

  return (
    <section className="py-20 px-4 bg-background">
      <div className="container mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-foreground mb-4">
            More Than Just Design Inspiration
          </h2>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            We don't just show you what could be - we give you everything you need to make it happen, with complete shopping lists and implementation guidance.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <Card key={index} className="shadow-elegant hover:shadow-glow transition-all duration-300 border-0 bg-card/80 backdrop-blur-sm">
              <CardHeader>
                <div className="text-4xl mb-4">{feature.icon}</div>
                <CardTitle className="text-xl">{feature.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground mb-4">
                  {feature.description}
                </p>
                <div className="flex flex-wrap gap-2">
                  {feature.benefits.map((benefit, idx) => (
                    <Badge key={idx} variant="secondary" className="text-xs">
                      {benefit}
                    </Badge>
                  ))}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
};