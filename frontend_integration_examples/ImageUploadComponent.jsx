// React Component for Image Upload and Design Generation
// Add this to your React frontend project

import React, { useState, useCallback } from 'react';
import { aiImageAPI } from './api_client';

const ImageUploadComponent = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [designStyle, setDesignStyle] = useState('modern');
  const [customInstructions, setCustomInstructions] = useState('');
  const [pathway, setPathway] = useState('standard'); // 'standard' or 'real-products'
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [analysisResults, setAnalysisResults] = useState(null); // For customize style screen
  const [error, setError] = useState(null);

  // Handle file selection
  const handleFileSelect = useCallback((event) => {
    const file = event.target.files[0];
    if (file && file.type.startsWith('image/')) {
      setSelectedFile(file);
      setError(null);
    } else {
      setError('Please select a valid image file');
    }
  }, []);

  // Handle drag and drop
  const handleDrop = useCallback((event) => {
    event.preventDefault();
    const file = event.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
      setSelectedFile(file);
      setError(null);
    } else {
      setError('Please drop a valid image file');
    }
  }, []);

  const handleDragOver = useCallback((event) => {
    event.preventDefault();
  }, []);

  // Generate design
  const handleGenerate = async () => {
    if (!selectedFile && !analysisResults) {
      setError('Please select an image first');
      return;
    }

    setLoading(true);
    setError(null);
    setResults(null);

    try {
      let response;
      
      if (pathway === 'standard') {
        response = await aiImageAPI.generateStandardDesign(
          selectedFile,
          designStyle,
          customInstructions
        );
      } else {
        // For real products pathway, use existing analysis if available
        if (analysisResults) {
          response = await aiImageAPI.generateWithExistingAnalysis(
            analysisResults.session_id,
            analysisResults,
            designStyle,
            customInstructions
          );
        } else {
          response = await aiImageAPI.generateRealProductsDesign(
            selectedFile,
            designStyle,
            customInstructions
          );
        }
      }

      if (response.success) {
        setResults(response.data);
        setAnalysisResults(null); // Clear analysis results after generation
      } else {
        setError(response.error || 'Generation failed');
      }
    } catch (err) {
      setError(err.message || 'An error occurred during generation');
    } finally {
      setLoading(false);
    }
  };

  // Analyze image only
  const handleAnalyze = async () => {
    if (!selectedFile) {
      setError('Please select an image first');
      return;
    }

    setLoading(true);
    setError(null);
    setResults(null); // Clear any previous results

    try {
      const response = await aiImageAPI.analyzeImage(
        selectedFile,
        designStyle,
        customInstructions
      );

      if (response.success) {
        setAnalysisResults(response.data);
      } else {
        setError(response.error || 'Analysis failed');
      }
    } catch (err) {
      setError(err.message || 'An error occurred during analysis');
    } finally {
      setLoading(false);
    }
  };

  // Reset to start over
  const handleReset = () => {
    setSelectedFile(null);
    setAnalysisResults(null);
    setResults(null);
    setError(null);
  };

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold mb-6 text-center">AI Interior Design Generator</h2>
      
      {/* File Upload Area */}
      <div
        className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
          selectedFile ? 'border-green-400 bg-green-50' : 'border-gray-300 hover:border-gray-400'
        }`}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
      >
        {selectedFile ? (
          <div>
            <p className="text-green-600 font-semibold">✅ {selectedFile.name}</p>
            <img
              src={URL.createObjectURL(selectedFile)}
              alt="Preview"
              className="max-w-xs max-h-48 mx-auto mt-4 rounded"
            />
          </div>
        ) : (
          <div>
            <p className="text-gray-500 mb-4">Drag and drop an image here, or click to select</p>
            <input
              type="file"
              accept="image/*"
              onChange={handleFileSelect}
              className="hidden"
              id="file-input"
            />
            <label
              htmlFor="file-input"
              className="bg-blue-500 text-white px-4 py-2 rounded cursor-pointer hover:bg-blue-600"
            >
              Select Image
            </label>
          </div>
        )}
      </div>

      {/* Configuration Options */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
        {/* Design Style */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Design Style
          </label>
          <select
            value={designStyle}
            onChange={(e) => setDesignStyle(e.target.value)}
            className="w-full p-2 border border-gray-300 rounded focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="modern">Modern</option>
            <option value="scandinavian">Scandinavian</option>
            <option value="bohemian">Bohemian</option>
            <option value="industrial">Industrial</option>
            <option value="minimalist">Minimalist</option>
            <option value="traditional">Traditional</option>
          </select>
        </div>

        {/* Pathway Selection */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Generation Mode
          </label>
          <select
            value={pathway}
            onChange={(e) => setPathway(e.target.value)}
            className="w-full p-2 border border-gray-300 rounded focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="standard">Standard (AI-imagined products)</option>
            <option value="real-products">Real Products (Actual shopping items)</option>
          </select>
        </div>
      </div>

      {/* Custom Instructions */}
      <div className="mt-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Custom Instructions (Optional)
        </label>
        <textarea
          value={customInstructions}
          onChange={(e) => setCustomInstructions(e.target.value)}
          placeholder="Add specific requirements or preferences..."
          className="w-full p-3 border border-gray-300 rounded focus:ring-blue-500 focus:border-blue-500"
          rows="3"
        />
      </div>

      {/* Customize Style Screen - Show when we have analysis results */}
      {analysisResults && !results && (
        <div className="mt-6 p-6 bg-blue-50 border border-blue-200 rounded-lg">
          <h3 className="text-xl font-bold mb-4 text-blue-800">🎨 Customize Your Design Style</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            {/* Room Analysis Summary */}
            {analysisResults.roomAnalysis && (
              <div className="bg-white p-4 rounded border">
                <h4 className="font-semibold mb-2 text-gray-800">Room Analysis</h4>
                <div className="text-sm space-y-1">
                  <p><strong>Room Type:</strong> {analysisResults.roomAnalysis.roomType}</p>
                  <p><strong>Current Style:</strong> {analysisResults.roomAnalysis.currentStyle}</p>
                  <p><strong>Mood:</strong> {analysisResults.roomAnalysis.mood}</p>
                </div>
              </div>
            )}
            
            {/* Recommendations Preview */}
            {analysisResults.recommendations && (
              <div className="bg-white p-4 rounded border">
                <h4 className="font-semibold mb-2 text-gray-800">Recommended Items</h4>
                <div className="text-sm">
                  <ul className="list-disc list-inside space-y-1">
                    {analysisResults.recommendations.slice(0, 4).map((rec, idx) => (
                      <li key={idx}>{rec.type}</li>
                    ))}
                    {analysisResults.recommendations.length > 4 && (
                      <li className="text-gray-500">...and {analysisResults.recommendations.length - 4} more</li>
                    )}
                  </ul>
                </div>
              </div>
            )}
          </div>

          <div className="mb-6">
            <p className="text-blue-700 mb-4">
              💡 <strong>Perfect!</strong> We've analyzed your room. Now you can adjust the design style and add custom instructions before we find real products and generate your design.
            </p>
            
            {/* Style and Instructions (repeated from above for easy editing) */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Design Style
                </label>
                <select
                  value={designStyle}
                  onChange={(e) => setDesignStyle(e.target.value)}
                  className="w-full p-2 border border-gray-300 rounded focus:ring-blue-500 focus:border-blue-500"
                  disabled={loading}
                >
                  <option value="modern">Modern</option>
                  <option value="scandinavian">Scandinavian</option>
                  <option value="bohemian">Bohemian</option>
                  <option value="industrial">Industrial</option>
                  <option value="minimalist">Minimalist</option>
                  <option value="traditional">Traditional</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Custom Instructions
                </label>
                <textarea
                  value={customInstructions}
                  onChange={(e) => setCustomInstructions(e.target.value)}
                  placeholder="Add specific requirements..."
                  className="w-full p-2 border border-gray-300 rounded focus:ring-blue-500 focus:border-blue-500"
                  rows="3"
                  disabled={loading}
                />
              </div>
            </div>
          </div>

          {/* Action buttons for customize style screen */}
          <div className="flex gap-4">
            <button
              onClick={handleReset}
              className="flex-1 bg-gray-500 text-white py-3 px-6 rounded font-semibold hover:bg-gray-600"
              disabled={loading}
            >
              🔄 Start Over
            </button>
            
            <button
              onClick={handleGenerate}
              disabled={loading}
              className="flex-2 bg-blue-600 text-white py-4 px-8 rounded-lg font-bold text-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed shadow-lg"
            >
              {loading ? '🛒 Generating Design...' : '🛒 Generate & Shop'}
            </button>
          </div>
        </div>
      )}

      {/* Action Buttons - Only show when no analysis results */}
      {!analysisResults && (
        <div className="flex gap-4 mt-6">
          <button
            onClick={handleAnalyze}
            disabled={loading || !selectedFile}
            className="flex-1 bg-green-500 text-white py-3 px-6 rounded font-semibold hover:bg-green-600 disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            {loading ? '🔍 Analyzing...' : '🔍 Analyze Only'}
          </button>
          
          <button
            onClick={handleGenerate}
            disabled={loading || !selectedFile}
            className="flex-1 bg-blue-500 text-white py-3 px-6 rounded font-semibold hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            {loading ? '🎨 Generating...' : '🎨 Generate Design'}
          </button>
        </div>
      )}

      {/* Error Display */}
      {error && (
        <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded">
          <p className="text-red-600">❌ {error}</p>
        </div>
      )}

      {/* Results Display */}
      {results && (
        <div className="mt-8 p-6 bg-gray-50 rounded-lg">
          <h3 className="text-xl font-semibold mb-4">Results</h3>
          
          {/* Show original image if available */}
          {(analysisResults?.original_image || results.original_image) && (
            <div className="mb-6">
              <h4 className="font-medium mb-2">Original Image:</h4>
              <img
                src={aiImageAPI.getImageURL(analysisResults?.original_image || results.original_image)}
                alt="Original uploaded image"
                className="max-w-sm rounded border"
              />
            </div>
          )}
          
          {/* Analysis Results */}
          {analysisResults && (
            <div className="mb-6">
              <h4 className="font-medium mb-2">Image Analysis:</h4>
              <pre className="bg-white p-4 rounded border text-sm overflow-auto">
                {JSON.stringify(analysisResults, null, 2)}
              </pre>
            </div>
          )}

          {/* Generated Design */}
          {results.serpapiProductsComposition && (
            <div className="mb-6">
              <h4 className="font-medium mb-2">Generated Design:</h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {results.serpapiProductsComposition.final_image && (
                  <div>
                    <p className="text-sm text-gray-600 mb-2">Final Design:</p>
                    <img
                      src={aiImageAPI.getImageURL(results.serpapiProductsComposition.final_image.filename)}
                      alt="Generated design"
                      className="w-full rounded border"
                    />
                  </div>
                )}
                
                {results.serpapiProductsComposition.composite_layout && (
                  <div>
                    <p className="text-sm text-gray-600 mb-2">Composite Layout:</p>
                    <img
                      src={aiImageAPI.getImageURL(results.serpapiProductsComposition.composite_layout)}
                      alt="Composite layout"
                      className="w-full rounded border"
                    />
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Products Used */}
          {results.serpapiProductsComposition?.products_info && (
            <div>
              <h4 className="font-medium mb-2">Products Used:</h4>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {results.serpapiProductsComposition.products_info.map((product, index) => (
                  <div key={index} className="bg-white p-4 rounded border">
                    <h5 className="font-medium text-sm">{product.name}</h5>
                    <p className="text-gray-600 text-sm">${product.price}</p>
                    <p className="text-gray-500 text-xs">{product.retailer}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ImageUploadComponent; 