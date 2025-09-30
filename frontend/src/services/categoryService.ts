import { strapi } from './strapi'

export interface Category {
  id: number
  attributes: {
    name: string
    createdAt: string
    updatedAt: string
    publishedAt: string
  }
}

// Alternative format that might be returned
export interface CategoryAlternative {
  id: number
  name: string
  createdAt?: string
  updatedAt?: string
  publishedAt?: string
}

export interface CategoryData {
  data: Category[]
  meta: {
    pagination: {
      page: number
      pageSize: number
      pageCount: number
      total: number
    }
  }
}

export interface CreateCategoryRequest {
  data: {
    name: string
  }
}

export const categoryService = {
  // Fetch all categories
  async getCategories(): Promise<CategoryData> {
    try {
      console.log('Fetching categories from:', '/categories')
      const response = await strapi.get<CategoryData>('/categories')
      console.log('Categories API response:', response.data)
      
      // Handle both Strapi v4 format (with data wrapper) and direct array
      if (response.data && typeof response.data === 'object') {
        if (Array.isArray(response.data)) {
          // Direct array format
          return {
            data: response.data,
            meta: {
              pagination: {
                page: 1,
                pageSize: response.data.length,
                pageCount: 1,
                total: response.data.length
              }
            }
          }
        } else if (response.data.data && Array.isArray(response.data.data)) {
          // Strapi v4 format with data wrapper
          return response.data
        }
      }
      
      // Fallback
      return {
        data: [],
        meta: {
          pagination: {
            page: 1,
            pageSize: 0,
            pageCount: 1,
            total: 0
          }
        }
      }
    } catch (error) {
      console.error('Error fetching categories:', error)
      throw error
    }
  },

  // Create a new category
  async createCategory(name: string): Promise<Category> {
    try {
      const response = await strapi.post<{data: Category}>('/categories', {
        data: { name }
      })
      return response.data.data
    } catch (error) {
      console.error('Error creating category:', error)
      throw error
    }
  },

  // Update a category
  async updateCategory(id: number, name: string): Promise<Category> {
    try {
      const response = await strapi.put<{data: Category}>(`/categories/${id}`, {
        data: { name }
      })
      return response.data.data
    } catch (error) {
      console.error('Error updating category:', error)
      throw error
    }
  },

  // Delete a category
  async deleteCategory(id: number): Promise<void> {
    try {
      await strapi.delete(`/categories/${id}`)
    } catch (error) {
      console.error('Error deleting category:', error)
      throw error
    }
  }
}