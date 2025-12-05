export interface Student {
  id: number;
  student_id: string;
  full_name: string;
  email: string;
  phone?: string;
  department?: string;
  class_name?: string;
  year?: string;
  division?: string;
  roll_number?: string;
  notes?: string;
}

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface User {
  id: number;
  email: string;
  role: string;
}
