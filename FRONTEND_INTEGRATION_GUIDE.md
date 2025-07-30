# Frontend Integration Guide

## 🚀 Quick Start

### 1. Start the Backend Server
```bash
# Set environment variables
export OPENAI_API_KEY="your-openai-api-key"
export SERPAPI_KEY="your-serpapi-key"

# Start the Python backend
./start_backend.sh
# OR
python3 api_server.py
```

**Backend will be available at:** `http://localhost:8000`

### 2. Add Frontend Integration Files

Copy these files to your React frontend project:

#### `src/utils/api_client.js`
```javascript
// Copy the contents from frontend_integration_examples/api_client.js
```

#### `src/components/ImageUploadComponent.jsx`
```javascript
// Copy the contents from frontend_integration_examples/ImageUploadComponent.jsx
```

### 3. Install Frontend Dependencies

If using Tailwind CSS (recommended for styling):
```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

### 4. Use the Component

Add to your main App component:
```javascript
import ImageUploadComponent from './components/ImageUploadComponent';

function App() {
  return (
    <div className="App">
      <ImageUploadComponent />
    </div>
  );
}
```

## 🔧 API Endpoints

### Available Endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/health` | GET | Detailed health status |
| `/analyze-image` | POST | Analyze image with GPT-4o Vision |
| `/generate-standard` | POST | Generate with AI-imagined products |
| `/generate-real-products` | POST | Generate with real products |
| `/shopping-lists` | GET | List generated shopping lists |
| `/shopping-list/{filename}` | GET | Get specific shopping list |
| `/images/{filepath}` | GET | Serve generated images |

### Request Format:

All image endpoints expect `multipart/form-data`:
```javascript
const formData = new FormData();
formData.append('file', imageFile);
formData.append('design_style', 'modern');
formData.append('custom_instructions', 'Add minimalist furniture');
formData.append('design_type', 'interior redesign');
```

### Response Format:

```javascript
{
  "success": true,
  "message": "Operation completed successfully",
  "data": {
    // Response data varies by endpoint
  },
  "error": null
}
```

## 🎨 Frontend Customization

### Design Styles Available:
- `modern`
- `scandinavian` 
- `bohemian`
- `industrial`
- `minimalist`
- `traditional`

### Generation Modes:
- **Standard Pathway**: AI-imagined products (faster, creative)
- **Real Products Pathway**: Actual shopping items (slower, real products)

## 🔄 Integration with Existing Frontend

### Option 1: Replace Existing Backend Calls

If you have existing backend integration, replace your API calls with the new `aiImageAPI` client:

```javascript
// Old way
const response = await fetch('/api/generate-design', { ... });

// New way
const response = await aiImageAPI.generateStandardDesign(file, style, instructions);
```

### Option 2: Add New Routes

Add new routes to your React Router:

```javascript
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ImageUploadComponent from './components/ImageUploadComponent';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/ai-design" element={<ImageUploadComponent />} />
        {/* Your existing routes */}
      </Routes>
    </Router>
  );
}
```

### Option 3: Integrate with Existing UI

Use the API client in your existing components:

```javascript
import { aiImageAPI } from '../utils/api_client';

const YourExistingComponent = () => {
  const handleDesignGeneration = async (imageFile) => {
    try {
      const result = await aiImageAPI.generateRealProductsDesign(
        imageFile, 
        'modern', 
        'Add contemporary furniture'
      );
      // Handle result
    } catch (error) {
      // Handle error
    }
  };

  // Your existing component logic
};
```

## 🛠️ Development Tips

### 1. CORS Configuration
The backend is already configured for React dev servers on ports 3000 and 3001.

### 2. Error Handling
Always wrap API calls in try-catch blocks:

```javascript
try {
  const result = await aiImageAPI.generateStandardDesign(file, style);
  if (result.success) {
    // Handle success
  } else {
    // Handle API error
  }
} catch (error) {
  // Handle network/other errors
}
```

### 3. Loading States
Show loading indicators during API calls:

```javascript
const [loading, setLoading] = useState(false);

const handleGenerate = async () => {
  setLoading(true);
  try {
    const result = await aiImageAPI.generateStandardDesign(file, style);
    // Handle result
  } finally {
    setLoading(false);
  }
};
```

### 4. File Validation
Validate image files before upload:

```javascript
const validateFile = (file) => {
  const validTypes = ['image/jpeg', 'image/png', 'image/webp'];
  const maxSize = 10 * 1024 * 1024; // 10MB

  if (!validTypes.includes(file.type)) {
    throw new Error('Please select a valid image file (JPEG, PNG, WebP)');
  }
  
  if (file.size > maxSize) {
    throw new Error('File size must be less than 10MB');
  }
  
  return true;
};
```

## 🚀 Production Deployment

### Backend Deployment:
1. Deploy Python backend to your preferred platform (AWS, Heroku, etc.)
2. Update `API_BASE_URL` in `api_client.js` to your production URL
3. Set environment variables on your production server

### Frontend Deployment:
1. Build your React app: `npm run build`
2. Deploy to your preferred platform (Vercel, Netlify, etc.)
3. Ensure CORS is configured for your production domain

## 🎯 Next Steps

1. **Test the Integration**: Start both backend and frontend, test image upload
2. **Customize UI**: Modify the React component to match your design
3. **Add Features**: Extend the API client for additional functionality
4. **Deploy**: Deploy both backend and frontend to production

## 📞 Support

If you need help with integration:
1. Check the backend API documentation: `http://localhost:8000/docs`
2. Test endpoints directly using the Swagger UI
3. Check browser console for error messages
4. Verify environment variables are set correctly

## 🔗 Useful Links

- **Backend API Docs**: `http://localhost:8000/docs`
- **Health Check**: `http://localhost:8000/health`
- **Interactive API Testing**: `http://localhost:8000/docs#/` 