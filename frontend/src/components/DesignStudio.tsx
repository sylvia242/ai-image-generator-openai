import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { useToast } from "@/hooks/use-toast";
import { useState, useEffect } from "react";
import { Upload, Wand2, ShoppingBag, ArrowRight, CheckCircle, Clock, Sparkles, AlertCircle } from "lucide-react";
import { aiImageAPI, type DesignResult } from "@/utils/api";

export const DesignStudio = () => {
  const { toast } = useToast();
  const [selectedRoom, setSelectedRoom] = useState("");
  const [selectedStyle, setSelectedStyle] = useState("");
  const [budget, setBudget] = useState("");
  const [activeTab, setActiveTab] = useState("upload");
  const [completedSteps, setCompletedSteps] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [designResult, setDesignResult] = useState<DesignResult | null>(null);
  const [generationError, setGenerationError] = useState<string | null>(null);
  const [fastMode, setFastMode] = useState<boolean>(false); // Default to fast mode
  const [generationProgress, setGenerationProgress] = useState({
    currentStep: 0,
    steps: [
      { id: 1, key: "Vision Analysis", title: "Analyzing Your Space", description: "AI examining room layout, colors, and style", completed: false },
      { id: 2, key: "Product Search", title: "Finding Perfect Products", description: "Searching thousands of real products that match your style", completed: false },
      { id: 3, key: "Composite Layout", title: "Creating Product Layout", description: "Organizing product recommendations with images", completed: false },
      { id: 4, key: "Final Design", title: "Generating Final Design", description: "AI creating your personalized room transformation", completed: false }
    ]
  });

  const steps = [
    { id: "upload", label: "Upload Photos", icon: Upload },
    { id: "customize", label: "Customize Style", icon: Wand2 },
    { id: "generate", label: "Generate & Shop", icon: ShoppingBag },
  ];

  const rooms = [
    { value: "living-room", label: "Living Room" },
    { value: "bedroom", label: "Bedroom" },
    { value: "kitchen", label: "Kitchen" },
    { value: "bathroom", label: "Bathroom" },
    { value: "dining-room", label: "Dining Room" },
    { value: "office", label: "Office" },
  ];

  const styles = [
    { value: "modern", label: "Modern" },
    { value: "bohemian", label: "Bohemian" },
    { value: "scandinavian", label: "Scandinavian" },
    { value: "industrial", label: "Industrial" },
    { value: "traditional", label: "Traditional" },
    { value: "minimalist", label: "Minimalist" },
  ];

  const budgets = [
    { value: "low", label: "Budget-Friendly ($100-500)" },
    { value: "medium", label: "Mid-Range ($500-1500)" },
    { value: "high", label: "Premium ($1500+)" },
  ];

  const isStepAccessible = (stepId: string) => {
    if (stepId === "upload") return true;
    if (stepId === "customize") return uploadedFile !== null;
    if (stepId === "generate") return uploadedFile !== null && !isLoading; // Allow manual navigation when not loading
    return false;
  };

  const handleNextStep = (stepId: string) => {
    if (!isStepAccessible(stepId)) return;
    setActiveTab(stepId);
  };

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setUploadedFile(file);
      setGenerationError(null);
      if (!completedSteps.includes("upload")) {
        setCompletedSteps(prev => [...prev, "upload"]);
      }
      toast({
        title: "Image uploaded successfully",
        description: `${file.name} uploaded! You can now customize your preferences before generating your design.`,
      });
      setActiveTab("customize");
    }
  };

  const handleCustomizationComplete = () => {
    // Mark customize step as completed when user makes selections
    if (uploadedFile) {
      if (!completedSteps.includes("customize")) {
        setCompletedSteps(prev => [...prev, "customize"]);
      }
    }
  };

  // Remove automatic navigation to generate tab
  // Users will only go to generate tab when they explicitly click "Generate Design & Shop Real Products"

  const generateDesign = async () => {
    if (!uploadedFile) {
      toast({
        title: "Missing image",
        description: "Please upload an image before generating design",
        variant: "destructive",
      });
      return;
    }

    // Mark customize step as completed
    handleCustomizationComplete();
    
    setIsLoading(true);
    setGenerationError(null);
    
    // Reset progress and switch to generate tab
    setGenerationProgress(prev => ({
      ...prev,
      currentStep: 1,
      steps: prev.steps.map(step => ({ ...step, completed: false }))
    }));
    setActiveTab("generate");

    // Start realistic progress tracking based on expected timings
    const startProgressTracking = () => {
      // Estimated timings based on actual backend performance
      const estimatedTimings = fastMode 
        ? { "Vision Analysis": 15000, "Product Search": 25000, "Composite Layout": 3000, "Final Design": 15000 }
        : { "Vision Analysis": 20000, "Product Search": 45000, "Composite Layout": 5000, "Final Design": 25000 };
      
      let currentStepIndex = 0;
      const stepKeys = ["Vision Analysis", "Product Search", "Composite Layout", "Final Design"];
      
      const updateProgress = () => {
        if (currentStepIndex < stepKeys.length) {
          const currentKey = stepKeys[currentStepIndex];
          
          setGenerationProgress(prev => ({
            ...prev,
            currentStep: currentStepIndex + 1,
            steps: prev.steps.map((step, index) => ({
              ...step,
              completed: index < currentStepIndex
            }))
          }));
          
          // Schedule next step
          setTimeout(() => {
            currentStepIndex++;
            updateProgress();
          }, estimatedTimings[currentKey]);
        }
      };
      
      updateProgress();
    };

    startProgressTracking();

    try {
      let result;
      
      result = await aiImageAPI.generateRealProductsDesign(
        uploadedFile,
        selectedRoom || "living-room", // Default to living room
        selectedStyle || "modern", // Default to modern style
        budget || "medium", // Default to medium budget
        fastMode, // Use dynamic fastMode state
        "" // Empty custom instructions - will be auto-generated from room and budget
      );

      setDesignResult(result.data);
      
      // Update progress based on actual backend step durations
      if (result.data.step_durations) {
        const stepDurations = result.data.step_durations;
        console.log('Backend step durations:', stepDurations);
        
        setGenerationProgress(prev => ({
          ...prev,
          currentStep: 5,
          steps: prev.steps.map(step => ({
            ...step,
            completed: true,
            duration: stepDurations[step.key] || 0
          }))
        }));
      } else {
        // Fallback: mark all as completed
        setGenerationProgress(prev => ({
          ...prev,
          currentStep: 5,
          steps: prev.steps.map(step => ({ ...step, completed: true }))
        }));
      }
      
      if (!completedSteps.includes("generate")) {
        setCompletedSteps(prev => [...prev, "generate"]);
      }

      toast({
        title: "Design generated successfully!",
        description: "Your personalized design is ready with real products",
      });

    } catch (error: any) {
      console.error('Design generation error:', error);
      setGenerationError(error.message || 'Failed to generate design');
      
      // Reset progress on error
      setGenerationProgress(prev => ({
        ...prev,
        currentStep: 0,
        steps: prev.steps.map(step => ({ ...step, completed: false }))
      }));
      
      toast({
        title: "Generation failed",
        description: error.message || "Please try again",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const currentProgress = (() => {
    if (completedSteps.includes("generate")) return 100;
    if (completedSteps.includes("customize")) return 66;
    if (completedSteps.includes("upload")) return 33;
    return 0;
  })();

  return (
    <section className="min-h-screen bg-background flex flex-col" data-section="design-studio">
      {/* Progress Header */}
      <div className="border-b border-border bg-card/50 backdrop-blur-sm">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between mb-3">
            <div>
              <h1 className="text-3xl font-bold text-foreground mb-2">Generate design for your space</h1>
              <p className="text-muted-foreground">Premium AI interior design service</p>
            </div>
            <div className="text-right">
              <div className="text-2xl font-bold text-primary">{currentProgress}%</div>
              <div className="text-sm text-muted-foreground">Complete</div>
            </div>
          </div>
          
          {/* Progress Bar */}
          <div className="w-full bg-muted rounded-full h-2 overflow-hidden">
            <div 
              className="h-full bg-gradient-accent transition-all duration-700 ease-out"
              style={{ width: `${currentProgress}%` }}
            />
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 container mx-auto px-6 py-6">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full max-w-6xl mx-auto">
          <TabsList className="grid w-full grid-cols-3 bg-card shadow-premium rounded-2xl p-2 border border-border/50 min-h-[80px] mb-8">
            {steps.map((step) => {
              const isCompleted = completedSteps.includes(step.id);
              const isActive = activeTab === step.id;
              const isAccessible = isStepAccessible(step.id);
              
              return (
                <TabsTrigger 
                  key={step.id}
                  value={step.id}
                  disabled={!isAccessible}
                  className={`
                    relative rounded-xl py-4 px-6 text-sm font-medium transition-all duration-300
                    ${isActive ? 'bg-primary text-primary-foreground shadow-glow' : ''}
                    ${isCompleted && !isActive ? 'bg-secondary/20 text-secondary' : ''}
                    ${!isAccessible ? 'opacity-40' : 'hover:bg-muted/50'}
                    disabled:pointer-events-none
                  `}
                  onClick={() => handleNextStep(step.id)}
                >
                  <div className="flex items-center gap-3">
                    {isCompleted ? (
                      <CheckCircle className="h-6 w-6 text-secondary animate-scale-in" />
                    ) : (
                      <step.icon className="h-6 w-6" />
                    )}
                    <span className="hidden sm:inline">{step.label}</span>
                  </div>
                  {isActive && (
                    <div className="absolute inset-0 rounded-xl bg-gradient-accent opacity-10 animate-fade-in" />
                  )}
                </TabsTrigger>
              );
            })}
          </TabsList>

          <div className="animate-fade-in">
            <TabsContent value="upload" className="space-y-12">
              <div className="text-center mb-12">
                <h2 className="text-4xl font-bold text-foreground mb-4">Share Your Space</h2>
                <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
                  Upload photos of your room for our AI design concierge to analyze and transform
                </p>
              </div>

              <div className="grid md:grid-cols-2 gap-12 max-w-4xl mx-auto">
                <Card className="group p-12 border-2 border-dashed border-primary/30 hover:border-primary/60 transition-all duration-300 hover:shadow-premium bg-gradient-to-br from-card to-muted/20">
                  <CardContent className="flex flex-col items-center justify-center text-center p-0">
                    <div className="relative">
                      <Upload className="h-16 w-16 text-primary mx-auto mb-6 group-hover:scale-110 transition-transform duration-300" />
                      <Sparkles className="h-6 w-6 text-secondary absolute -top-2 -right-2 animate-pulse" />
                    </div>
                    <CardTitle className="text-2xl mb-3">Upload Your Room</CardTitle>
                    <CardDescription className="mb-6">
                      Select a high-quality photo of your space. After upload, you'll be taken to customize your preferences before generating your design.
                    </CardDescription>
                    <input
                      type="file"
                      accept="image/*"
                      onChange={handleFileUpload}
                      className="hidden"
                      id="file-upload"
                    />
                    <label htmlFor="file-upload">
                      <Button 
                        asChild
                        size="lg" 
                        className="cursor-pointer shadow-glow hover:shadow-premium transition-all duration-300"
                      >
                        <span>Choose Image</span>
                      </Button>
                    </label>
                    {uploadedFile && (
                      <div className="mt-4 p-3 bg-secondary/10 rounded-lg border border-secondary/20">
                        <p className="text-sm text-secondary font-medium">✓ {uploadedFile.name}</p>
                      </div>
                    )}
                  </CardContent>
                </Card>

                <Card className="group p-12 hover:shadow-premium transition-all duration-300 bg-gradient-to-br from-card to-secondary/5">
                  <CardContent className="flex flex-col items-center justify-center text-center p-0">
                    <div className="relative">
                      <Wand2 className="h-16 w-16 text-secondary mx-auto mb-6 group-hover:scale-110 transition-transform duration-300" />
                      <div className="absolute inset-0 bg-secondary/20 rounded-full blur-xl animate-pulse" />
                    </div>
                    <CardTitle className="text-2xl mb-3">Try Sample Room</CardTitle>
                    <CardDescription className="mb-6">
                      Explore our AI capabilities with a sample room design
                    </CardDescription>
                    <Button 
                      variant="secondary" 
                      size="lg"
                      className="shadow-glow hover:shadow-premium transition-all duration-300"
                      onClick={() => {
                        // Create a sample file for demo
                        const canvas = document.createElement('canvas');
                        canvas.width = 800;
                        canvas.height = 600;
                        canvas.toBlob((blob) => {
                          if (blob) {
                            const file = new File([blob], 'sample-room.png', { type: 'image/png' });
                            setUploadedFile(file);
                            setGenerationError(null);
                            toast({
                              title: "Sample room loaded",
                              description: "Ready for design generation with sample image",
                            });
                            if (!completedSteps.includes("upload")) {
                              setCompletedSteps(prev => [...prev, "upload"]);
                            }
                            setActiveTab("customize");
                          }
                        });
                      }}
                    >
                      Use Sample
                    </Button>
                  </CardContent>
                </Card>
              </div>

              <div className="text-center">
                <div className="mt-4 text-sm text-muted-foreground">
                  <p>• Supported formats: JPG, PNG, WebP</p>
                  <p>• Maximum file size: 10MB</p>
                  <p>• For best results, use well-lit, high-resolution images</p>
                </div>
              </div>
            </TabsContent>

            <TabsContent value="customize" className="space-y-8">
              <div className="text-center mb-6">
                <h2 className="text-3xl font-bold text-foreground mb-3">Customize Your Style</h2>
                <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
                  Tell us about your preferences to create the perfect design. All fields are optional - we'll use smart defaults if not specified.
                </p>
              </div>

              <div className="grid md:grid-cols-3 gap-4 max-w-5xl mx-auto">
                <Card className="p-6 hover:shadow-premium transition-all duration-300 border-2 hover:border-primary/30">
                  <div className="flex items-center gap-3 mb-4">
                    <div className="w-3 h-3 bg-primary rounded-full"></div>
                    <CardTitle className="text-lg">Room Type <span className="text-sm text-muted-foreground font-normal">(Optional)</span></CardTitle>
                  </div>
                  <Select value={selectedRoom} onValueChange={setSelectedRoom}>
                    <SelectTrigger className="w-full">
                      <SelectValue placeholder="Select room type" />
                    </SelectTrigger>
                    <SelectContent>
                      {rooms.map((room) => (
                        <SelectItem key={room.value} value={room.value}>
                          {room.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  {selectedRoom && (
                    <div className="mt-4 flex items-center gap-2 text-secondary animate-fade-in">
                      <CheckCircle className="h-4 w-4" />
                      <span className="text-sm">Room type selected</span>
                    </div>
                  )}
                </Card>

                <Card className="p-6 hover:shadow-premium transition-all duration-300 border-2 hover:border-secondary/30">
                  <div className="flex items-center gap-3 mb-4">
                    <div className="w-3 h-3 bg-secondary rounded-full"></div>
                    <CardTitle className="text-lg">Design Style <span className="text-sm text-muted-foreground font-normal">(Optional)</span></CardTitle>
                  </div>
                  <Select value={selectedStyle} onValueChange={setSelectedStyle}>
                    <SelectTrigger className="w-full">
                      <SelectValue placeholder="Choose your style" />
                    </SelectTrigger>
                    <SelectContent>
                      {styles.map((style) => (
                        <SelectItem key={style.value} value={style.value}>
                          {style.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  {selectedStyle && (
                    <div className="mt-4 flex items-center gap-2 text-secondary animate-fade-in">
                      <CheckCircle className="h-4 w-4" />
                      <span className="text-sm">Style preference set</span>
                    </div>
                  )}
                </Card>

                <Card className="p-6 hover:shadow-premium transition-all duration-300 border-2 hover:border-accent/30">
                  <div className="flex items-center gap-3 mb-4">
                    <div className="w-3 h-3 bg-accent rounded-full"></div>
                    <CardTitle className="text-lg">Investment Level <span className="text-sm text-muted-foreground font-normal">(Optional)</span></CardTitle>
                  </div>
                  <Select value={budget} onValueChange={setBudget}>
                    <SelectTrigger className="w-full">
                      <SelectValue placeholder="Select budget range" />
                    </SelectTrigger>
                    <SelectContent>
                      {budgets.map((budgetOption) => (
                        <SelectItem key={budgetOption.value} value={budgetOption.value}>
                          {budgetOption.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  {budget && (
                    <div className="mt-4 flex items-center gap-2 text-secondary animate-fade-in">
                      <CheckCircle className="h-4 w-4" />
                      <span className="text-sm">Budget range confirmed</span>
                    </div>
                  )}
                </Card>
              </div>

              <div className="text-center mt-8">
                {/* Fast Mode Toggle */}
                <div className="flex items-center justify-center gap-3 mb-6 p-4 bg-muted/30 rounded-lg border">
                    <div className="flex items-center gap-2">
                      <span className="text-sm font-medium">Analysis Speed:</span>
                      <div className="flex items-center gap-2">
                        <span className={`text-xs ${!fastMode ? 'text-primary font-medium' : 'text-muted-foreground'}`}>
                          Detailed
                        </span>
                        <button
                          onClick={() => setFastMode(!fastMode)}
                          className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                            fastMode ? 'bg-primary' : 'bg-muted-foreground/30'
                          }`}
                        >
                          <span
                            className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                              fastMode ? 'translate-x-6' : 'translate-x-1'
                            }`}
                          />
                        </button>
                        <span className={`text-xs ${fastMode ? 'text-primary font-medium' : 'text-muted-foreground'}`}>
                          Fast ⚡
                        </span>
                      </div>
                    </div>
                    <div className="text-xs text-muted-foreground">
                      {fastMode ? 'GPT-4o Mini • ~30s faster' : 'GPT-4o • Most detailed'}
                    </div>
                  </div>
                  
                  <div className="flex flex-col items-center gap-4">
                    <Button 
                      size="lg" 
                      onClick={generateDesign}
                      disabled={isLoading}
                      className="shadow-glow hover:shadow-premium transition-all duration-300 px-8 py-4 text-lg"
                    >
                      {isLoading ? (
                        <>
                          <div className="animate-spin rounded-full h-5 w-5 border-2 border-primary-foreground border-t-transparent mr-2"></div>
                          Generating Design...
                        </>
                      ) : (
                        <>
                          🎨 Generate Design & Shop Real Products
                          <ArrowRight className="ml-2 h-5 w-5" />
                        </>
                      )}
                    </Button>
                    
                    {!isLoading && (
                      <div className="mt-4 text-sm text-muted-foreground">
                        <p>✨ Ready to generate design for your space? Click the button above to start generating your design with real products!</p>
                      </div>
                    )}
                    
                    {isLoading && (
                      <div className="mt-4 text-xs text-muted-foreground space-y-1">
                        <p>🔍 Analyzing your space...</p>
                        <p>🛒 Finding real products...</p>
                        <p>🎨 Creating your design...</p>
                        <p className="text-secondary">
                          ⏱️ This may take {fastMode ? '1-2 minutes' : '2-3 minutes'} 
                          {fastMode ? ' (Fast Mode ⚡)' : ' (Detailed Mode)'}
                        </p>
                      </div>
                    )}
                    
                    {generationError && (
                      <div className="text-center mt-8">
                        <div className="flex flex-col items-center gap-4">
                          <AlertCircle className="h-12 w-12 text-destructive" />
                          <div>
                            <h3 className="text-lg font-semibold text-destructive mb-2">
                              Generation Failed
                            </h3>
                            <p className="text-sm text-muted-foreground mb-4">{generationError}</p>
                            <Button 
                              onClick={generateDesign}
                              variant="outline"
                              className="hover:bg-destructive/10"
                            >
                              Try Again
                            </Button>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
            </TabsContent>

            <TabsContent value="generate" className="space-y-12">
              <div className="text-center mb-12">
                <h2 className="text-4xl font-bold text-foreground mb-4">Your AI Design</h2>
                <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
                  Discover your transformed space with carefully curated real products
                </p>
              </div>

              {/* Progress Indicator */}
              {isLoading && (
                <div className="max-w-4xl mx-auto mb-12">
                  <Card className="p-8 border-2 border-primary/20 shadow-premium">
                    <div className="text-center mb-8">
                      <div className="inline-flex items-center gap-3 px-6 py-3 bg-primary/10 rounded-full mb-4">
                        <div className="animate-spin rounded-full h-5 w-5 border-2 border-primary border-t-transparent"></div>
                        <span className="text-lg font-semibold text-primary">
                          {fastMode ? 'Fast Mode ⚡' : 'Detailed Mode 🔍'} - Creating Your Design
                        </span>
                      </div>
                      <p className="text-muted-foreground">
                        Estimated time: {fastMode ? '1-2 minutes' : '2-3 minutes'}
                      </p>
                    </div>

                    <div className="space-y-6">
                      {generationProgress.steps.map((step, index) => (
                        <div key={step.id} className="flex items-center gap-4">
                          <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center border-2 transition-all duration-500 ${
                            step.completed 
                              ? 'bg-green-500 border-green-500 text-white' 
                              : generationProgress.currentStep === step.id
                              ? 'border-primary bg-primary/10 text-primary animate-pulse'
                              : 'border-muted-foreground/30 text-muted-foreground'
                          }`}>
                            {step.completed ? (
                              <CheckCircle className="h-4 w-4" />
                            ) : generationProgress.currentStep === step.id ? (
                              <div className="animate-spin rounded-full h-3 w-3 border border-primary border-t-transparent"></div>
                            ) : (
                              <span className="text-sm font-medium">{step.id}</span>
                            )}
                          </div>
                          
                          <div className="flex-1">
                            <div className={`font-medium transition-colors duration-300 ${
                              step.completed ? 'text-green-600' : generationProgress.currentStep === step.id ? 'text-primary' : 'text-muted-foreground'
                            }`}>
                              {step.title}
                            </div>
                            <div className="text-sm text-muted-foreground mt-1">
                              {step.description}
                            </div>
                          </div>
                          
                          {step.completed && (
                            <div className="text-green-500 text-sm font-medium animate-fade-in">
                              ✓ Complete {(step as any).duration ? `(${((step as any).duration).toFixed(1)}s)` : ''}
                            </div>
                          )}
                        </div>
                      ))}
                    </div>

                    <div className="mt-8">
                      <div className="w-full bg-muted rounded-full h-2 overflow-hidden">
                        <div 
                          className="h-full bg-gradient-to-r from-primary to-secondary transition-all duration-1000 ease-out"
                          style={{ 
                            width: `${(generationProgress.steps.filter(s => s.completed).length / generationProgress.steps.length) * 100}%` 
                          }}
                        ></div>
                      </div>
                      <div className="text-center mt-3 text-sm text-muted-foreground">
                        Step {generationProgress.currentStep > generationProgress.steps.length ? generationProgress.steps.length : generationProgress.currentStep} of {generationProgress.steps.length}
                        {designResult?.total_duration && (
                          <span className="block mt-1 text-green-600 font-medium">
                            Total: {designResult.total_duration.toFixed(1)}s
                          </span>
                        )}
                      </div>
                    </div>
                  </Card>
                </div>
              )}

              {designResult ? (
                <div className="grid lg:grid-cols-2 gap-12 max-w-6xl mx-auto">
                  {/* Generated Design Image */}
                  <Card className="overflow-hidden shadow-premium border-2 border-primary/20">
                    <CardHeader className="bg-gradient-hero text-primary-foreground">
                      <CardTitle className="flex items-center gap-2">
                        <Sparkles className="h-5 w-5" />
                        AI Generated Design
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="p-0">
                      <div className="aspect-[4/3] bg-gradient-hero rounded-xl mb-6 flex items-center justify-center border border-border/50 overflow-hidden">
                        {isLoading ? (
                          <div className="flex flex-col items-center gap-4">
                            <div className="animate-spin rounded-full h-12 w-12 border-4 border-primary border-t-transparent"></div>
                            <p className="text-sm text-muted-foreground">Generating your design...</p>
                          </div>
                        ) : (
                          <div className="flex flex-col items-center gap-4 p-6 text-center">
                            {designResult.final_design ? (
                              <img 
                                src={`http://localhost:8000/images/${designResult.final_design}`}
                                alt="Generated Design"
                                className="w-full h-full object-cover rounded-lg"
                                onError={(e) => {
                                  console.error('Image load error:', e);
                                  e.currentTarget.style.display = 'none';
                                  e.currentTarget.parentElement?.insertAdjacentHTML('afterbegin', 
                                    '<div class="w-full h-full flex items-center justify-center bg-muted rounded-lg"><p class="text-muted-foreground">Image not available</p></div>'
                                  );
                                }}
                              />
                            ) : (
                              <div className="w-full h-full flex items-center justify-center bg-muted rounded-lg">
                                <div className="text-center">
                                  <p className="text-muted-foreground mb-2">Design generation failed</p>
                                  <p className="text-xs text-muted-foreground">Please try again</p>
                                </div>
                              </div>
                            )}
                          </div>
                        )}
                      </div>
                      
                      <div className="p-6 bg-muted/30">
                        <div className="flex items-center justify-between text-sm">
                          <div className="flex items-center gap-2 text-secondary">
                            <CheckCircle className="h-4 w-4" />
                            <span>AI Enhanced</span>
                          </div>
                          <div className="flex items-center gap-2 text-secondary">
                            <Clock className="h-4 w-4" />
                            <span>Just generated</span>
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>

                  {/* Product Shopping List */}
                  <Card className="shadow-premium border-2 border-secondary/20">
                    <CardHeader className="bg-gradient-to-r from-secondary/10 to-accent/10">
                      <div className="flex items-center justify-between">
                        <CardTitle className="flex items-center gap-2">
                          <ShoppingBag className="h-5 w-5 text-secondary" />
                          Real Products
                        </CardTitle>
                        <Badge variant="secondary" className="animate-pulse">
                          {designResult.products_info?.length || 0} Items
                        </Badge>
                      </div>
                      <CardDescription>
                        Curated products to recreate this design in your space
                      </CardDescription>
                    </CardHeader>
                    <CardContent className="p-6">
                      <div className="space-y-4">
                        <div className="flex items-center justify-between">
                          <h3 className="font-semibold text-lg">Shopping List</h3>
                          <div className="flex items-center gap-2">
                            <Badge variant="outline" className="text-xs">
                              {selectedStyle?.charAt(0).toUpperCase() + selectedStyle?.slice(1)} Style
                            </Badge>
                          </div>
                        </div>
                        
                        <div className="flex items-center gap-4 text-xs text-muted-foreground">
                          <span>🎯 Style-matched products</span>
                          <span>💰 Budget-optimized</span>
                          <span>⭐ Highly rated</span>
                        </div>

                        <div className="grid gap-4 max-h-96 overflow-y-auto">
                          {designResult.products_info?.map((product, index) => (
                            <Card key={index} className="p-4 hover:shadow-md transition-all duration-200 border border-border/50">
                              <div className="flex items-start gap-4">
                                {/* Product Image */}
                                <div className="flex-shrink-0">
                                  {product.image_path ? (
                                    <img 
                                      src={`http://localhost:8000/images/${product.image_path}`}
                                      alt={product.name}
                                      className="w-16 h-16 object-cover rounded-lg border border-border/20"
                                      onError={(e) => {
                                        e.currentTarget.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIHZpZXdCb3g9IjAgMCA2NCA2NCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHJlY3Qgd2lkdGg9IjY0IiBoZWlnaHQ9IjY0IiBmaWxsPSIjRjNGNEY2Ii8+CjxwYXRoIGQ9Ik0yMCAyMEg0NFY0NEgyMFYyMFoiIHN0cm9rZT0iIzlDQTNBRiIgc3Ryb2tlLXdpZHRoPSIyIiBmaWxsPSJub25lIi8+CjxjaXJjbGUgY3g9IjI2IiBjeT0iMjgiIHI9IjIiIGZpbGw9IiM5Q0EzQUYiLz4KPHBhdGggZD0iTTIwIDM2TDI4IDI4TDM2IDM2TDQ0IDI4VjQ0SDIwVjM2WiIgZmlsbD0iIzlDQTNBRiIvPgo8L3N2Zz4K';
                                      }}
                                    />
                                  ) : (
                                    <div className="w-16 h-16 bg-muted rounded-lg border border-border/20 flex items-center justify-center">
                                      <span className="text-xs text-muted-foreground">No image</span>
                                    </div>
                                  )}
                                </div>
                                
                                {/* Product Details */}
                                <div className="flex-1 min-w-0">
                                  <div className="flex items-start justify-between">
                                    <div className="flex-1 min-w-0">
                                      <h4 className="font-medium text-sm text-foreground truncate">{product.name}</h4>
                                      <p className="text-xs text-muted-foreground mt-1">{product.retailer}</p>
                                      <div className="flex items-center gap-2 mt-1">
                                        <span className="text-sm font-semibold text-primary">{product.price}</span>
                                        {product.rating && (
                                          <div className="flex items-center gap-1">
                                            <span className="text-xs text-secondary">⭐ {product.rating}</span>
                                            {product.reviews && (
                                              <span className="text-xs text-muted-foreground">({product.reviews})</span>
                                            )}
                                          </div>
                                        )}
                                      </div>
                                    </div>
                                    
                                    <div className="flex flex-col gap-2 ml-4">
                                      <Button 
                                        size="sm" 
                                        variant="outline"
                                        className="text-xs px-3 py-1 h-auto"
                                        onClick={() => {
                                          if (product.url) {
                                            window.open(product.url, '_blank', 'noopener,noreferrer');
                                          }
                                        }}
                                      >
                                        View Product
                                      </Button>
                                    </div>
                                  </div>
                                </div>
                              </div>
                            </Card>
                          ))}
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </div>
              ) : !isLoading ? (
                <div className="text-center mt-8">
                  <Card className="max-w-2xl mx-auto p-12 border-2 border-dashed border-border/50">
                    <div className="flex flex-col items-center gap-6">
                      <div className="w-20 h-20 rounded-full bg-muted flex items-center justify-center">
                        <Wand2 className="h-10 w-10 text-muted-foreground" />
                      </div>
                      <div>
                        <h3 className="text-xl font-semibold mb-2">Ready to Generate Design for Your Space?</h3>
                        <p className="text-muted-foreground mb-6">
                          Upload an image and click "Generate Design" to see your room with real products
                        </p>
                        <div className="flex flex-wrap justify-center gap-2">
                          <Badge variant="outline" className="px-3 py-1">
                            ✨ AI-Powered Analysis
                          </Badge>
                          <Badge variant="outline" className="px-3 py-1">
                            🛒 Real Products
                          </Badge>
                          <Badge variant="outline" className="px-3 py-1">
                            🎨 Instant Results
                          </Badge>
                        </div>
                      </div>
                    </div>
                  </Card>
                </div>
              ) : null}
            </TabsContent>
          </div>
        </Tabs>
      </div>
    </section>
  );
}; 