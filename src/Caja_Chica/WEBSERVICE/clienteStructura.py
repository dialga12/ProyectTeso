import barrister

trans  = barrister.HttpTransport("http://localhost:7667/add")

# automatically connects to endpoint and loads IDL JSON contract
client = barrister.Client(trans)

print client.Calculator.add({'clase':'ok','metodo':'restar','codusuarios':['1','2']})


print
print "IDL metadata:"
meta = client.get_meta()
for key in [ "barrister_version", "checksum" ]:
    print "%s=%s" % (key, meta[key])

# not printing this one because it changes per run, which breaks our
# very literal 'examples' test harness, but let's verify it exists at least..
assert meta.has_key("date_generated")


