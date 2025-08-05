import { Button } from "@/components/ui/button";
import { Upload, Sparkles } from "lucide-react";
import { useNavigate } from "react-router-dom";

export const Hero = () => {
  const navigate = useNavigate();
  return (
    <section className="bg-gradient-hero py-20 px-4">
      <div className="container mx-auto text-center">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-5xl md:text-6xl font-bold text-foreground mb-6 leading-tight">
            Transform Any Space with <span className="text-accent font-bold">AI-Powered Design</span>
          </h2>
          
          <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
            Get instant design transformations with complete shopping lists. We bridge the gap between design inspiration and real-life transformation.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-16">
            <Button size="lg" className="shadow-elegant" onClick={() => navigate('/start-design')}>
              Try One Room Free
            </Button>
            <Button variant="outline" size="lg">
              Register for More Credits
            </Button>
          </div>

          {/* Before & After Preview */}
          <div className="max-w-4xl mx-auto">
            <h3 className="text-2xl font-semibold text-center mb-8">See the Magic in Action</h3>
            <div className="grid md:grid-cols-2 gap-8 items-center">
              <div className="text-center">
                <h4 className="text-lg font-medium mb-4 text-muted-foreground">Before</h4>
                <div className="aspect-[4/3] bg-muted rounded-lg overflow-hidden shadow-elegant">
                  <img 
                    src="https://images.unsplash.com/photo-1721322800607-8c38375eef04?w=500&h=375&fit=crop&auto=format" 
                    alt="Room before transformation"
                    className="w-full h-full object-cover"
                  />
                </div>
              </div>
              <div className="text-center">
                <h4 className="text-lg font-medium mb-4 text-accent">After</h4>
                <div className="aspect-[4/3] bg-muted rounded-lg overflow-hidden shadow-elegant">
                  <img 
                    src="https://images.unsplash.com/photo-1483058712412-4245e9b90334?w=500&h=375&fit=crop&auto=format" 
                    alt="Room after transformation"
                    className="w-full h-full object-cover"
                  />
                </div>
              </div>
            </div>
            <div className="text-center mt-8">
              <p className="text-muted-foreground">
                Complete with shopping list • 3 design variations • Ready to buy
              </p>
            </div>

            {/* Key Products Section */}
            <div className="mt-12">
              <h4 className="text-xl font-semibold text-center mb-8 text-foreground">
                Key Products That Made the Difference
              </h4>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-3xl mx-auto">
                <div className="group p-6 bg-card rounded-xl shadow-elegant hover:shadow-premium transition-all duration-300 border border-border/50">
                  <div className="aspect-square bg-muted rounded-lg overflow-hidden mb-4">
                    <img 
                      src="https://images.unsplash.com/photo-1581090464777-f3220bbe1b8b?w=300&h=300&fit=crop&auto=format" 
                      alt="Modern Sectional Sofa"
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                    />
                  </div>
                  <h5 className="font-semibold text-foreground mb-2">Modern Sectional Sofa</h5>
                  <p className="text-primary font-bold mb-2">$1,299</p>
                  <p className="text-sm text-muted-foreground">The foundation piece that anchors the room's new layout</p>
                </div>

                <div className="group p-6 bg-card rounded-xl shadow-elegant hover:shadow-premium transition-all duration-300 border border-border/50">
                  <div className="aspect-square bg-muted rounded-lg overflow-hidden mb-4">
                    <img 
                      src="https://images.unsplash.com/photo-1618160702438-9b02ab6515c9?w=300&h=300&fit=crop&auto=format" 
                      alt="Statement Floor Lamp"
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                    />
                  </div>
                  <h5 className="font-semibold text-foreground mb-2">Statement Floor Lamp</h5>
                  <p className="text-primary font-bold mb-2">$289</p>
                  <p className="text-sm text-muted-foreground">Adds warm lighting and modern elegance to the space</p>
                </div>

                <div className="group p-6 bg-card rounded-xl shadow-elegant hover:shadow-premium transition-all duration-300 border border-border/50">
                  <div className="aspect-square bg-muted rounded-lg overflow-hidden mb-4">
                    <img 
                      src="https://images.unsplash.com/photo-1582562124811-c09040d0a901?w=300&h=300&fit=crop&auto=format" 
                      alt="Decorative Wall Art"
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                    />
                  </div>
                  <h5 className="font-semibold text-foreground mb-2">Decorative Wall Art</h5>
                  <p className="text-primary font-bold mb-2">$159</p>
                  <p className="text-sm text-muted-foreground">Creates visual interest and completes the design story</p>
                </div>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-16">
            <div className="text-center">
              <div className="bg-card rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4 shadow-elegant">
                <Sparkles className="h-8 w-8 text-primary" />
              </div>
              <h3 className="text-lg font-semibold mb-2">AI Design Magic</h3>
              <p className="text-muted-foreground">
                Instant room transformations using advanced AI
              </p>
            </div>
            
            <div className="text-center">
              <div className="bg-card rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4 shadow-elegant">
                <span className="text-2xl">🛍️</span>
              </div>
              <h3 className="text-lg font-semibold mb-2">Shoppable Lists</h3>
              <p className="text-muted-foreground">
                Every item is purchasable with direct retailer links
              </p>
            </div>
            
            <div className="text-center">
              <div className="bg-card rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4 shadow-elegant">
                <span className="text-2xl">⚡</span>
              </div>
              <h3 className="text-lg font-semibold mb-2">Instant Results</h3>
              <p className="text-muted-foreground">
                Get your transformed space in seconds
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};