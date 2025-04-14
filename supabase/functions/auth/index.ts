import "jsr:@supabase/functions-js/edge-runtime.d.ts";

console.info('server started');

Deno.serve(async (req)=>{
  try {
    const { name } = await req.json();

    const data = {
      message: `Hello ${name}!`
    };
    return new Response(JSON.stringify(data), {
      headers: {
        'Content-Type': 'application/json',
        'Connection': 'keep-alive'
      }
    });
  } catch (error) {
    return new Response(JSON.stringify({
      error: 'Invalid request payload'
    }), {
      status: 400,
      headers: {
        'Content-Type': 'application/json'
      }
    });
  }
});
