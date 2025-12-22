export type WSHandlers = {
  onOpen: () => void;
  onClose: () => void;
  onError: () => void;
  onMessage: (response: ServerMessage) => void;
};

export type Chunk = {
  chunk_id: string,
  section: string,
  title: string
}
export type Citation = {
  doc_title: string,
  source_path: string,
  parent_id: string
  chunks: Chunk[]
}
export type ServerMessage = {
  content: string,
  citations: Citation[]
}

export type ChatMessage = 
  | { id: string; role: "user"; content: string; createdAt: number }
  | { id: string; role: "assistant"; content: string; citations?: Citation[]; createdAt: number };
