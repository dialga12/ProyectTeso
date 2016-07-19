import barrister

trans  = barrister.HttpTransport("http://localhost:7667/lista")

# automatically connects to endpoint and loads IDL JSON contract
client = barrister.Client(trans)

print client.Lista.lista(7,8)
print client.Lista.lista(8, 20)

print
print "IDL metadata:"
meta = client.get_meta()
for key in [ "barrister_version", "checksum" ]:
    print "%s=%s" % (key, meta[key])

# not printing this one because it changes per run, which breaks our
# very literal 'examples' test harness, but let's verify it exists at least..
assert meta.has_key("date_generated")


