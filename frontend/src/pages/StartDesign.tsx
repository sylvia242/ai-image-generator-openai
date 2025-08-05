import { Button } from "@/components/ui/button";
import { DesignStudio } from "@/components/DesignStudio";
import { ArrowLeft } from "lucide-react";
import { useNavigate } from "react-router-dom";

const StartDesign = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-background">
      {/* Header with back navigation */}
      <div className="border-b border-border bg-card/50 backdrop-blur-sm">
        <div className="container mx-auto px-6 py-2">
          <Button
            variant="ghost"
            onClick={() => navigate('/')}
            className="flex items-center gap-2 hover:bg-muted"
          >
            <ArrowLeft className="h-4 w-4" />
            Back to Home
          </Button>
        </div>
      </div>
      
      {/* Design Studio Component */}
      <DesignStudio />
    </div>
  );
};

export default StartDesign;