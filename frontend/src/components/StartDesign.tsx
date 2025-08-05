import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Upload, Wand2, ShoppingBag, ArrowRight, Sparkles } from "lucide-react";
import { useNavigate } from "react-router-dom";

export const StartDesign = () => {
  const navigate = useNavigate();

  const handleStartDesign = () => {
    // Navigate to the Start Design page
    navigate('/start-design');
  };

  return (
    <section className="py-20 bg-gradient-to-br from-background to-muted/20" data-section="start-design">
      <div className="container mx-auto px-6">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-foreground mb-6">
            Ready to Transform Your Space?
          </h2>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            Our AI design concierge will guide you through a personalized experience in just 3 simple steps
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto mb-16">
          <Card className="group hover:shadow-premium transition-all duration-300 p-8 border border-border/50">
            <CardHeader className="text-center">
              <div className="relative mb-6">
                <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto group-hover:scale-110 transition-transform duration-300">
                  <Upload className="h-8 w-8 text-primary" />
                </div>
                <div className="absolute -top-2 -right-2 w-8 h-8 bg-secondary rounded-full flex items-center justify-center">
                  <span className="text-secondary-foreground font-bold text-sm">1</span>
                </div>
              </div>
              <CardTitle className="text-xl mb-3">Upload Your Room</CardTitle>
              <CardDescription className="text-base">
                Share photos of your current space for AI analysis
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="group hover:shadow-premium transition-all duration-300 p-8 border border-border/50">
            <CardHeader className="text-center">
              <div className="relative mb-6">
                <div className="w-16 h-16 bg-secondary/10 rounded-full flex items-center justify-center mx-auto group-hover:scale-110 transition-transform duration-300">
                  <Wand2 className="h-8 w-8 text-secondary" />
                </div>
                <div className="absolute -top-2 -right-2 w-8 h-8 bg-accent rounded-full flex items-center justify-center">
                  <span className="text-accent-foreground font-bold text-sm">2</span>
                </div>
              </div>
              <CardTitle className="text-xl mb-3">Customize Style</CardTitle>
              <CardDescription className="text-base">
                Choose your preferred design aesthetic and budget
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="group hover:shadow-premium transition-all duration-300 p-8 border border-border/50">
            <CardHeader className="text-center">
              <div className="relative mb-6">
                <div className="w-16 h-16 bg-accent/10 rounded-full flex items-center justify-center mx-auto group-hover:scale-110 transition-transform duration-300">
                  <ShoppingBag className="h-8 w-8 text-accent" />
                </div>
                <div className="absolute -top-2 -right-2 w-8 h-8 bg-primary rounded-full flex items-center justify-center">
                  <span className="text-primary-foreground font-bold text-sm">3</span>
                </div>
              </div>
              <CardTitle className="text-xl mb-3">Get Results</CardTitle>
              <CardDescription className="text-base">
                Receive your transformation with curated shopping list
              </CardDescription>
            </CardHeader>
          </Card>
        </div>

        <div className="text-center">
          <Button 
            size="lg" 
            onClick={handleStartDesign}
            className="px-12 py-6 text-xl hover:shadow-glow transition-all duration-300"
          >
            <Sparkles className="mr-3 h-6 w-6" />
            Start Your Design Journey
            <ArrowRight className="ml-3 h-6 w-6" />
          </Button>
          <p className="text-muted-foreground mt-4 text-lg">
            Free trial • No credit card required • Instant results
          </p>
        </div>
      </div>
    </section>
  );
};