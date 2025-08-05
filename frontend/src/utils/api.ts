// API Client for AI Image Generator Backend
const API_BASE_URL = 'http://localhost:8000';

export interface APIResponse<T = any> {
  success: boolean;
  message: string;
  data?: T;
  error?: string;
}

export interface DesignResult {
  success: boolean;
  original_image: string;
  final_design: string;
  products_info: Array<{
    name: string;
    price: string;
    retailer: string;
    url: string;
    rating?: number;
    reviews?: number;
    image_path: string;
  }>;
  products_used: number;
  design_style: string;
  analysis_results: any;
  step_durations?: Record<string, number>;
  total_duration?: number;
  session_id?: string;
  session_path?: string;
}

class AIImageGeneratorAPI {
  private baseURL: string;

  constructor() {
    this.baseURL = API_BASE_URL;
  }

  // Health check
  async healthCheck(): Promise<APIResponse> {
    try {
      const response = await fetch(`${this.baseURL}/health`);
      return await response.json();
    } catch (error) {
      console.error('Health check failed:', error);
      throw error;
    }
  }

  // Generate design using real products pathway
  async generateRealProductsDesign(
            imageFile: File, 
            roomType: string = 'living-room',
            designStyle: string = 'modern', 
            budget: string = 'medium',
            fastMode: boolean = true,
            customInstructions: string = ''
          ): Promise<APIResponse<DesignResult>> {
            try {
              const formData = new FormData();
              formData.append('file', imageFile);
              formData.append('design_style', designStyle);
              formData.append('custom_instructions', customInstructions || `${roomType} design with ${budget} budget`);
              formData.append('design_type', 'interior redesign');
              formData.append('fast_mode', fastMode.toString());
        
              console.log('Sending request to:', `${this.baseURL}/generate-real-products`);
              console.log('Form data:', {
                roomType,
                designStyle,
                budget,
                customInstructions,
                fastMode,
                fileName: imageFile.name,
                fileSize: imageFile.size
              });
        
              // Create timeout controller for better browser compatibility
              const controller = new AbortController();
              const timeoutId = setTimeout(() => controller.abort(), 300000); // 5 minutes
              
              const response = await fetch(`${this.baseURL}/generate-real-products`, {
                method: 'POST',
                body: formData,
                signal: controller.signal
              });
              
              clearTimeout(timeoutId);
        
              console.log('Response status:', response.status);
              console.log('Response headers:', Object.fromEntries(response.headers.entries()));
        
              if (!response.ok) {
                let errorMessage = `HTTP error! status: ${response.status}`;
                try {
                  const errorData = await response.json();
                  errorMessage = errorData.error || errorData.detail || errorMessage;
                } catch (e) {
                  // If we can't parse JSON, use the status text
                  errorMessage = response.statusText || errorMessage;
                }
                throw new Error(errorMessage);
              }
        
              const result = await response.json();
              console.log('API response:', result);
              
              // The backend returns an APIResponse wrapper, so we need to return the data
              if (result.success && result.data) {
                console.log('Backend data structure:', result.data);
                console.log('Final design path:', result.data.final_design);
                console.log('Products info:', result.data.products_info);
                return {
                  success: true,
                  message: result.message,
                  data: result.data
                };
              } else {
                throw new Error(result.error || 'Generation failed');
              }
            } catch (error) {
              console.error('Real products design generation failed:', error);
              
              // Handle specific error types
              if (error instanceof Error) {
                if (error.name === 'AbortError') {
                  throw new Error('Request timed out after 5 minutes - the design may still be processing. Please try again in a moment.');
                } else if (error.message.includes('Failed to fetch') || error.message.includes('fetch')) {
                  throw new Error('Connection failed - please check if the backend server is running on http://localhost:8000');
                } else if (error.message.includes('NetworkError')) {
                  throw new Error('Network error - please check your connection and try again');
                }
              }
              
              throw error;
            }
          }

  // Generate design using standard pathway (AI-imagined products)
  async generateStandardDesign(
    imageFile: File, 
    designStyle: string = 'modern', 
    customInstructions: string = '', 
    designType: string = 'interior redesign'
  ): Promise<APIResponse<DesignResult>> {
    try {
      const formData = new FormData();
      formData.append('file', imageFile);
      formData.append('design_style', designStyle);
      formData.append('custom_instructions', customInstructions);
      formData.append('design_type', designType);

      const response = await fetch(`${this.baseURL}/generate-standard`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Standard design generation failed:', error);
      throw error;
    }
  }

  // Get image URL
  getImageURL(filepath: string): string {
    return `${this.baseURL}/images/${filepath}`;
  }

  // Get shopping list URL
  getShoppingListURL(filename: string): string {
    return `${this.baseURL}/shopping-list/${filename}`;
  }
}

// Export singleton instance
export const aiImageAPI = new AIImageGeneratorAPI();

// Export class for custom instances
export default AIImageGeneratorAPI; 