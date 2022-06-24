def evaluateMultinomial(net, prime_str, predict_len, temperature=0.8):
  hidden = net.init_hidden()
  predicted = prime_str

  # "Building up" the hidden state
  for p in range(len(prime_str) - 1):
    inp = char_tensor(prime_str[p])
    _, hidden = net(inp, hidden)

  # Tensorize of the last character
  inp = char_tensor(prime_str[-1])

  # For every index to predict
  for p in range(predict_len):
    # Pass the character + previous hidden state to the model
    output, hidden = net(inp, hidden)

    # Sample from the network as a multinomial distribution
    output_dist = output.data.view(-1).div(temperature).exp()
    top_i = torch.multinomial(output_dist, 1)[0]

    # Add predicted character to string and use as next input
    predicted_char = all_characters[top_i]
    predicted += predicted_char
    inp = char_tensor(predicted_char)

  return predicted


## Uncomment to run
sampleDecoder = GenerationRNN(27, 100, 27, 1)
text = evaluateMultinomial(sampleDecoder, 'hi', 10)
if text.startswith('hi') and len(text) == 12:
  print('Success!')
else:
  print('Need to change.')