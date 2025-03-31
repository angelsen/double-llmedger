import { z } from 'zod';

export const loginSchema = z.object({
  username: z.string().min(3).max(31).regex(/^[a-z0-9_-]+$/, {
    message: 'Username can only contain lowercase letters, numbers, underscores, and dashes'
  }),
  password: z.string().min(6).max(255)
});

export const registerSchema = z.object({
  username: z.string().min(3).max(31).regex(/^[a-z0-9_-]+$/, {
    message: 'Username can only contain lowercase letters, numbers, underscores, and dashes'
  }),
  password: z.string().min(6).max(255)
});

export type LoginSchema = typeof loginSchema;
export type RegisterSchema = typeof registerSchema;