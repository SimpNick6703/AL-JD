
export interface Article {
  id: string;
  title: string;
  description: string;
  content: string; // Markdown content
}

export enum View {
  Home = 'HOME',
  List = 'LIST',
  Detail = 'DETAIL',
}

export enum EditAction {
  Summarize = 'SUMMARIZE',
  Expand = 'EXPAND',
  Rephrase = 'REPHRASE',
  FixGrammar = 'FIX_GRAMMAR',
}
