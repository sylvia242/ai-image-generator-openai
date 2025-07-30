// API Client for AI Image Generator Backend
// Add this to your React frontend project

const API_BASE_URL = 'http://localhost:8000';

class AIImageGeneratorAPI {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  // Health check
  async healthCheck() {
    try {
      const response = await fetch(`${this.baseURL}/health`);
      return await response.json();
    } catch (error) {
      console.error('Health check failed:', error);
      throw error;
    }
  }

  // Analyze image with GPT-4o Vision
  async analyzeImage(imageFile, designStyle, customInstructions = '', designType = 'interior redesign') {
    try {
      const formData = new FormData();
      formData.append('file', imageFile);
      formData.append('design_style', designStyle);
      formData.append('custom_instructions', customInstructions);
      formData.append('design_type', designType);

      const response = await fetch(`${this.baseURL}/analyze-image`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Image analysis failed:', error);
      throw error;
    }
  }

  // Generate design using standard pathway (AI-imagined products)
  async generateStandardDesign(imageFile, designStyle, customInstructions = '', designType = 'interior redesign') {
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
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Standard design generation failed:', error);
      throw error;
    }
  }

  // Generate design using real products pathway
  async generateRealProductsDesign(imageFile, designStyle, customInstructions = '', designType = 'interior redesign') {
    try {
      const formData = new FormData();
      formData.append('file', imageFile);
      formData.append('design_style', designStyle);
      formData.append('custom_instructions', customInstructions);
      formData.append('design_type', designType);

      const response = await fetch(`${this.baseURL}/generate-real-products`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Real products design generation failed:', error);
      throw error;
    }
  }

  // Get list of shopping lists
  async getShoppingLists() {
    try {
      const response = await fetch(`${this.baseURL}/shopping-lists`);
      return await response.json();
    } catch (error) {
      console.error('Failed to fetch shopping lists:', error);
      throw error;
    }
  }

  // Get specific shopping list
  getShoppingListURL(filename) {
    return `${this.baseURL}/shopping-list/${filename}`;
  }

  // Get image URL
  getImageURL(filepath) {
    return `${this.baseURL}/images/${filepath}`;
  }
}

// Export singleton instance
export const aiImageAPI = new AIImageGeneratorAPI();

// Export class for custom instances
export default AIImageGeneratorAPI; 