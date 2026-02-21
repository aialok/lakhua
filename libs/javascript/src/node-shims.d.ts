declare module "node:fs" {
  export const existsSync: (path: string) => boolean;
  export const readFileSync: (path: string, encoding: string) => string;
}

declare module "node:path" {
  export const dirname: (path: string) => string;
  export const join: (...parts: string[]) => string;
}

declare module "node:url" {
  export const fileURLToPath: (url: string | URL) => string;
}

