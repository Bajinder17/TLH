-- Create reports table
CREATE TABLE public.reports (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  scan_type TEXT NOT NULL CHECK (scan_type IN ('file', 'url', 'port')),
  scan_data JSONB NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  user_id UUID REFERENCES auth.users(id)
);

-- Create indexes for better query performance
CREATE INDEX reports_scan_type_idx ON public.reports (scan_type);
CREATE INDEX reports_created_at_idx ON public.reports (created_at DESC);
CREATE INDEX reports_user_id_idx ON public.reports (user_id);

-- Enable Row Level Security
ALTER TABLE public.reports ENABLE ROW LEVEL SECURITY;

-- Create policy for anonymous access (for demo purposes - you might want to restrict this in production)
-- This allows anyone to select reports but requires authentication for insert/update/delete
CREATE POLICY "Allow anonymous read access" 
  ON public.reports 
  FOR SELECT 
  USING (true);

-- Create policy for authenticated users to insert their own reports
CREATE POLICY "Allow authenticated users to insert reports"
  ON public.reports
  FOR INSERT
  TO authenticated
  WITH CHECK (true);

-- Create policy for users to update their own reports
CREATE POLICY "Allow users to update their own reports"
  ON public.reports
  FOR UPDATE
  TO authenticated
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

-- Create policy for users to delete their own reports
CREATE POLICY "Allow users to delete their own reports"
  ON public.reports
  FOR DELETE
  TO authenticated
  USING (auth.uid() = user_id);

-- Function to automatically set user_id on insert
CREATE OR REPLACE FUNCTION public.set_user_id()
RETURNS TRIGGER AS $$
BEGIN
  NEW.user_id = auth.uid();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger to set user_id when a new report is created
CREATE TRIGGER set_user_id_trigger
BEFORE INSERT ON public.reports
FOR EACH ROW
EXECUTE FUNCTION public.set_user_id();

-- Create a function to return all reports or just a user's reports based on authentication
CREATE OR REPLACE FUNCTION public.get_reports(filter_scan_type text DEFAULT NULL)
RETURNS SETOF reports AS $$
BEGIN
  IF filter_scan_type IS NULL THEN
    RETURN QUERY SELECT * FROM public.reports ORDER BY created_at DESC;
  ELSE
    RETURN QUERY SELECT * FROM public.reports WHERE scan_type = filter_scan_type ORDER BY created_at DESC;
  END IF;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Add a simple view for recent reports
CREATE VIEW public.recent_reports AS
SELECT id, scan_type, created_at, 
  CASE 
    WHEN scan_type = 'file' THEN scan_data->>'filename'
    WHEN scan_type = 'url' THEN scan_data->>'url'
    WHEN scan_type = 'port' THEN scan_data->>'target'
    ELSE 'Unknown'
  END AS scan_target,
  CASE
    WHEN scan_type = 'file' THEN (scan_data->'result'->>'status') = 'clean'
    WHEN scan_type = 'url' THEN (scan_data->'result'->>'status') = 'safe'
    WHEN scan_type = 'port' THEN (scan_data->'result'->>'status') = 'completed'
    ELSE false
  END AS is_safe
FROM public.reports
ORDER BY created_at DESC
LIMIT 100;

-- Enable realtime subscriptions for the reports table
ALTER PUBLICATION supabase_realtime ADD TABLE public.reports;
